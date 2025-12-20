from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

#prompt
prompt_str = "이 음식의 '{review}'에 대해 '{score1}'점부터 '{score2}'점까지의 평가를 해주세요"
prompt = PromptTemplate(
  input_variables=['review','score1','score2'], # 여러개의 변수가 있다면 리스트로 전달
  template=prompt_str
)

#llm
llm = ChatOpenAI(api_key=api_key,
                 model='gpt-4o-mini',
                 temperature=0.7)

#chain
chain = prompt | llm | StrOutputParser()

#사용자의 리뷰에 대한 평가를 요청
try:
  result = chain.invoke({
    'review':"맛은 있었지만 배달 포장이 부족해서 아쉬웠다.",
    "score1":"1",
    "score2":"5"
  })
  print(f"평가 결과:{result}")  
except Exception as e:
  print(f"Error:{e}")
