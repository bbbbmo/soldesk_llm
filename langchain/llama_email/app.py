import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.ctransformers import CTransformers
# from langchain_ollama.llms import OllamaLLM


def getLLMResponse(form_input, email_sender, email_recipient, language):
    """
    getLLMResponse 함수는 주어진 입력을 사용하여 LLM(대형 언어 모델)으로부터 이메일 응답을 생성합니다.

    매개변수:
    - form_input: 사용자가 입력한 이메일 주제.
    - email_sender: 이메일을 보낸 사람의 이름.
    - email_recipient: 이메일을 받는 사람의 이름.
    - language: 이메일이 생성될 언어 (한국어 또는 영어).

    반환값:
    - LLM이 생성한 이메일 응답 텍스트.
    """
    
    # Llama 2사용, 한국어 생성 안좋음
    llm = CTransformers(model='./llama-2-7b-chat.ggmlv3.q5_K_S.bin',
                        model_type='llama',
                        config={'max_new_tokens': 512,
                                'temperature': 0.01})

    # ollama llama3.1 부분 연결
    # llm = OllamaLLM(model="llama3.1:8b", temperature=0.7)

    if language == "한국어":
        template = """ 
        {email_topic} 주제를 포함한 이메일을 작성해 주세요.\n\n보낸 사람: {sender}\n받는 사람: {recipient} 전부 {language}로 번역해서 작성해주세요. 한문은 내용에서 제외해주세요.
        \n\n이메일 내용:
        """
    else: 
        template = """ 
        Write an email including the topic {email_topic}.\n\nSender: {sender}\nRecipient: {recipient} Please write the entire email in {language}.\n\nEmail content:
        """

    # 최종 PROMPT 생성
    prompt = PromptTemplate(
        input_variables=["email_topic", "sender", "recipient", "language"],
        template=template,
    )

    # LLM을 사용하여 응답 생성
    response = llm.invoke(prompt.format(email_topic=form_input, sender=email_sender, recipient=email_recipient, language=language))
    print(response)

    return response


st.set_page_config(
    page_title="이메일 생성기 📮",
    page_icon='📮',
    layout='centered',
    initial_sidebar_state='collapsed' #사이드바 접혀서 숨겨진상태 시작
)
st.header("이메일 생성기 📮 ")

# 이메일 작성 언어 선택 
language_option = st.selectbox(
    "이메일 작성 언어를 선택해주세요",
    ("한국어", "English"),
)

# 이메일 주제를 입력할 text_area 생성
form_input = st.text_area(
    "이메일 주제를 입력하세요", height=100,
)


# 한 라인에 두개의 입력을 만들기위해 st.columns()에 동일한 값의 list를 전달
col1, col2 = st.columns([10, 10])
with col1:
    email_sender = st.text_input('보낸 사람 이름')
with col2:
    email_recipient = st.text_input('받는 사람 이름')

# '생성하기' 버튼 생성
submit = st.button("생성하기")
# '생성하기' 버튼이 클릭->생성중..... -> getLLMResponse() 호출 -> 결과 출력
if submit:
    with st.spinner('생성 중 입니다...'):
        response = getLLMResponse(form_input, email_sender, email_recipient, language_option)


