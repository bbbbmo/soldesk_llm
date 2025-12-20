from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain, SequentialChain
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

#llm
llm = ChatOpenAI(api_key=api_key,
                 model='gpt-4o-mini',
                 temperature=0.7)

#prompt1
prompt1 = PromptTemplate.from_template(
  "다음 식당 리뷰를 한 문장으로 요약하세요.\n\n{review}"
)
chain1 = LLMChain(llm=llm,prompt=prompt1,output_key="summary")

#prompt2
prompt2 = PromptTemplate.from_template(
  "다음 식당 리뷰를 읽고 0점~10점사이에서 긍정/부정 점수를 매기세요 숫자로.\n\n{review}"
)
chain2 = LLMChain(llm=llm,
                  prompt=prompt2,
                  output_key="score")
#prompt3
prompt3 = PromptTemplate.from_template(
  "다음 식당 리뷰 요약에 대해 공손한 답변을 작성하세요\n리뷰요약{summary}"
)
chain3 = LLMChain(llm=llm,prompt=prompt3,output_key="reply")

#체인설정
all_chain = SequentialChain(
  chains=[chain1,chain2,chain3],
  input_variables=['review'],
  output_variables=['summary', "score", 'reply']
)

#input review:식당 리뷰
review ="""
이 식당은 맛도 좋고 분위기로 좋았습니다. 가격대비 만족도가 높아요.
하지만, 서비스 속도가 너무 느려서 조금 실망스러웠습니다.
전반적으로는 다시 방문할 의사가 있습니다.
"""

#체인 실행 및 결과 출력
try:
  result = all_chain.invoke({
    'review': review
  })
  print(f"review 요약 \n{result['summary']}\n")  
  print(f"review 점수 \n{result['score']}\n")  
  print(f"review 답변 \n{result['reply']}")  
  
except Exception as e:
  print(f"Error:{e}")
