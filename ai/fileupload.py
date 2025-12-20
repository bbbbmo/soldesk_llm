from flask import current_app
import pymupdf
import tool


def allowed_file(filename):   # ccc.bbb.aaa.jpg => [ccc.bbb.aaa, jpg]
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# 25 M 제한
def allowed_size(size):
    return True if size <= 1024 * 1024 * 25 else False

  
def pdf_to_text(pdf_file_path: str):
    doc = pymupdf.open(pdf_file_path)

    header_height = 80
    footer_height = 80

    full_text = ''

    for page in doc:
        rect = page.rect # 페이지 크기 가져오기
        
        #rect.width:400,rect.height:800 이라고 가정시
        #clip(시작x, 시작y, 끝x, 끝y), 0,0(왼쪽 상단(x,y)),clip(0,0,400,80)
        header = page.get_text(clip=(0, 0, rect.width , header_height))
        #clip(0,720(800-80),400,80)
        footer = page.get_text(clip=(0, rect.height - footer_height, rect.width , footer_height))
        #clip(0,80,400,720)
        text = page.get_text(clip=(0, header_height, rect.width , rect.height - footer_height))
    
        full_text += text + '\n------------------------------------\n'


    txt_file_path = f'static/pdf/pdf_text.txt'

    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    return txt_file_path

def summarize_txt(file_path: str, ): 
    
    # 주어진 텍스트 파일을 읽어들인다.
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    # 요약을 위한 시스템 프롬프트를 생성한다.

    role = '요약 시스템이야'
    prompt = f''' 
     아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라. 

    작성해야 하는 포맷은 다음과 같다. 
    <ol style='margin: auto; width:800px; text-align:left;'>
    <li> 제목 :
    <br>
    <li>저자의 문제 인식 및 주장 (15문장 이내) : 
    <br>
    <li> 저자 소개:
    </ol>
    <br>   
    =============== 이하 텍스트 ===============

    { txt }
    '''

    return tool.answer(role,prompt,output='text')