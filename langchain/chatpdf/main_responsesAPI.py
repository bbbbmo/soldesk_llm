from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

api_key = os.getenv('OpenAI_API_KEY')

client = OpenAI(api_key=api_key)

#제목 설정
st.header('소설 동백꽃 내용 확인')

#대화 히스토리 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

#지난 대화 히스토리 출력
if 'response_id' in st.session_state:
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.write(message['content'])
                
#질문 입력
prompt = st.text_input('질문', placeholder='질문을 입력해주세요')

if prompt:
    #사용자 질문 출력 및 히스토리 저장
    with st.chat_message('user'):
        st.write(prompt)
    st.session_state.chat_history.append({'role': 'user', 'content': prompt})

    #지난 대화가 없을 때
    if 'response_id' not in st.session_state:
        with st.spinner('Wait for it...'):
          response = client.responses.create(
            model="gpt-4o-mini",
            instructions='당신은 벡터 저장소의 내용을 알려줄 helper야',
            input=prompt,
            tools=[{
                "type": "file_search",
                "vector_store_ids": ["벡터저장소ID"]
            }]
          )
    else:     
          response = client.responses.create(
            previous_response_id=st.session_state.response_id,#이전 대화내용 가져오기 
            model="gpt-4o-mini",
            instructions='당신은 벡터 저장소의 내용을 알려줄 helper야',
            input=prompt,
            tools=[{
                "type": "file_search",
                "vector_store_ids": ["벡터저장소ID"]
            }]
          )

    # LLM 답변 출력 및 히스토리 저장
    with st.chat_message('assistant'):
        st.write(response.output_text)
    st.session_state.chat_history.append({'role': 'assistant', 'content': response.output_text})
    st.session_state.response_id = response.id