import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

st.title("AI 시인 :sunglasses:")

title = st.text_input("시의 주제를 입력해주세요", "겨울")
st.write("시의 주제: ", title)

if st.button("시 작성"):
    with st.spinner("시 작성 중", show_time=True):
        llm = init_chat_model("gpt-4o-mini", api_key=api_key)

        prompt = ChatPromptTemplate.from_messages([ # 프롬프트 템플릿을 제공
            ("system", "너는 나를 도와주는 어시스턴트야."),
            ("user", "{input}"),
        ])

        # 문자열 출력 파서
        output_parser = StrOutputParser()

        chain = prompt | llm | output_parser
        result = chain.invoke({"input": title + "에 대한 시를 생성해줘"})
        st.write(result)