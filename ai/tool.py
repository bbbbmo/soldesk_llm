import json
from openai import OpenAI
from dotenv import load_dotenv
import os
# OpenAI API 사용함수
# role: GPT 역활  예) 너는 문화 해설가야 - 필수
# prompt: 질문 메시지 - 필수
# format='': 출력 세부 형식, 파라미터 전달이 안되면 아무 값도 사용하지 않는다는 선언
# llm='gpt-4o-mini': 사용할 인공지능 모델
# output='json': 출력 형식
def answer(role, prompt, format='json', llm='gpt-4o-mini', output='json'):
    
    # openai key 가져오기
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
        
    client = OpenAI(api_key = api_key)

    if output.lower() == 'json':
        # gpt-3.5-turbo, gpt-4o-mini-2024-07-18, gpt-4-turbo, gpt-4o
        response = client.chat.completions.create(
            model=llm,
            messages=[
                {
                    'role': 'system',
                    'content': role
                },
                {
                    'role': 'user',
                    'content': prompt + '\n\n출력 형식(json): ' + format
                }
            ],
            n=1,             # 응답수, 다양한 응답 생성 가능
            max_tokens=1000, # 응답 생성시 최대 1000개의 단어 사용
            temperature=0,   # 창의적인 응답여부, 값이 클수록 확률에 기반한 창의적인 응답이 생성됨
            response_format= { "type":"json_object" }
        )
        print('json')
        return json.loads(response.choices[0].message.content) # str -> json
    else:
        response = client.chat.completions.create(
        model=llm,
        messages=[
            {
                'role': 'system',
                'content': role
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        
        temperature=0.1    # 창의적인 응답여부, 값이 클수록 확률에 기반한 창의적인 응답이 생성됨
    )
    return response.choices[0].message.content 
  
# 문자열을 라인단위로 분리하여, 빈 라인을 제거하고, 문장들로 이루어진 리스트 생성
# 토큰 아끼기 위해 사용
def remove_empty_lines(text):
    lines = [line for line in text.splitlines() if line.strip()]
    # print('-> lines:', lines)
    # print('-' * 80)
    # 문장들을 다시 합쳐서 하나의 문자열로 반환
    result = '\n'.join(lines)
    return result

