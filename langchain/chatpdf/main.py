import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic import hub
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

loader = PyPDFLoader('dong.pdf')
pages = loader.load_and_split()
 
# print(pages[0]) #pages[1]:두번째 페이지, pages[2] 세번째....

text_splitter = RecursiveCharacterTextSplitter(
# Set a really small chunk size, just to show.
chunk_size=100, #각 청크의 최대 길이
chunk_overlap=20, #인접한 청크사이의 중복영역, 문장이 끊기는 문제 해결 20글자 겹침
length_function=len,#청크길이 측정하는 함수
is_separator_regex=False,#단순한 문자열로 해석
    )
texts = text_splitter.split_documents(pages)

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large") # 문서를 임베딩해 벡터 형태로 변환
                                                                                                                   
db = Chroma.from_documents(texts, embeddings_model) # 임베딩 벡터를 저장, 인자로 븐할된 청크 리스트를 받음

question = "점순이가 주인공에게 느끼는 감정은 무엇이야?"
llm = ChatOpenAI(temperature=0, api_key=api_key) # 창의적인 대답 설정 

# Chroma 백터 저장소에 대한 Retriever 인스턴스 생성
retriever_from_llm = MultiQueryRetriever.from_llm( # 질문을 여러개 만들 수 있음 -> 관련성이 높은 결과를 제공
    retriever=db.as_retriever(), llm=llm
)

#사용자 질문에 대한 연관정보를 가져온다.
docs = retriever_from_llm.invoke(question)

#Prompt Template
prompt = hub.pull('rlm/rag-prompt')

#Generate
def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

rag_chain = (
{'context':retriever_from_llm | format_docs, "question":RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
)

#Question
result = rag_chain.invoke({"question": question})
print(result)