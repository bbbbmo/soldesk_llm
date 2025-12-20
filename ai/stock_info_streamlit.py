from gpt_functions import get_current_time, tools, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
# (0) api_key 
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") 

# (1) OpenAI 객체 생성 및 질문요청 함수 선언
client = OpenAI(api_key=api_key)
def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 응답 생성에 사용할 모델 지정
        messages=messages,  # 대화 기록을 입력으로 전달
        tools=tools,  # 사용 가능한 도구 목록 전달
    )
    return response  # 생성된 응답 내용 반환

st.title("💬 Chatbot")

# (2) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "너는 사용자를 도와주는 상담사야."}] 

# (3) 대화 기록을 출력
for msg in st.session_state.messages:
    #함수 role, system role은 출력 안한다.
    if msg["role"] == "assistant" or msg["role"] == "user": 
        st.chat_message(msg["role"]).write(msg["content"])

# (4) 사용자 입력을 받아 대화 기록에 추가하고 AI 응답을 생성
if prompt := st.chat_input():  
    if not api_key: 
        st.info("OpenAI Key가 필요합니다.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = get_ai_response(st.session_state.messages, tools=tools)
    msg = response.choices[0].message
    print(msg)
    
    # (5) AI 응답에 포함된 tool_calls를 가져옵니다.
    tool_calls = msg.tool_calls  
    if tool_calls:  
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 함수명
            tool_call_id = tool_call.id         # 아이디    
            arguments = json.loads(tool_call.function.arguments) # 문자열 -> 딕셔너리   
            
            #(6)함수 실행 설정
            if tool_name == "get_current_time":  
                func_result = get_current_time(timezone=arguments['timezone'])
            elif tool_name == "get_yf_stock_info":
                func_result = get_yf_stock_info(ticker=arguments['ticker'])
            elif tool_name == "get_yf_stock_history":  # get_yf_stock_history 함수 호출
                func_result = get_yf_stock_history(
                    ticker=arguments['ticker'], 
                    period=arguments['period']
                )
            elif tool_name == "get_yf_stock_recommendations":  # get_yf_stock_recommendations 함수 호출
                func_result = get_yf_stock_recommendations(
                    ticker=arguments['ticker']
                )

            # (7)함수관련 내용 messages 추가
            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": func_result,
            })


        st.session_state.messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."}) 
        response = get_ai_response(st.session_state.messages, tools=tools) # 다시 GPT 응답 받기
        msg = response.choices[0].message

    st.session_state.messages.append({
        "role": "assistant",
        "content": msg.content
    })  # ③ AI 응답을 대화 기록에 추가합니다.

    print("AI\t: ", msg.content)  # AI 응답 출력
    st.chat_message("assistant").write(msg.content)  # 브라우저에 메시지 출력