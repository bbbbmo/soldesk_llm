import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

llm = init_chat_model("gpt-4o-mini", api_key=api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 나를 도와주는 어시스턴트야."),
    ("user", "{input}"),
])

# 문자열 출력 파서
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
result = chain.invoke({"input": "안녕하세요. 너는 누구야?"})
print(result)