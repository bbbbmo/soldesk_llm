from flask import Blueprint, request, jsonify
from flask import render_template
import tool
import mail
import time
import os
import fileupload

# Flask Blueprint는 Flask 애플리케이션을 기능 단위로 분리·구조화하기 위한 모듈화 도구
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def hello():
    return render_template('hello.html')

@routes_bp.route('/summary') 
def summary():
    return render_template('summary.html')

@routes_bp.post('/summary')
def proc_summary():
  data = request.json
  article = data['article']

  # 빈라인 삭제
  article = tool.remove_empty_lines(article)
  prompt = f'아래 뉴스 기사를 200자 내외로 요약해줘. \n\n{article}'
  format = '''
    {
        "res": "요약된 뉴스 기사"
    }
  '''

  response = tool.answer('너는 요약 시스템이야',prompt,format)
  print(response)
  return response


@routes_bp.get('/translator')
def trans():
    return render_template('translator.html')

@routes_bp.post('/translator')
def proc_trans():
  data = request.json
  sentence = data['sentence']
  language = data['language']
  age = data['age']
  
  sentence = tool.remove_empty_lines(sentence)
  prompt = f"아래문장을 {age} 수준의 {language}로 번역해줘. \n\n{sentence}"
  format = '''
    {
        "res": "번역된 문장"
    }
  '''
  
  response = tool.answer('너는 번역기야',prompt, format)

  print(response)
  
  return response

@routes_bp.get('/mail')
def mail_page():
    return render_template('mail.html')

@routes_bp.post('/mail')
def proc_mail():
    data = request.json
    subject = data['subject']
    recipient_email = data['recipient_email']
    message = data['message']
    
    # 제목, 내용 번역하기
    subject = mail.use_api(subject)
    message = mail.use_api(message)
    print(subject)
    print(message)
    # 메일 보내기
    if subject and recipient_email and message:
        if mail.send_email(subject, recipient_email, message):
            print('Email send successfully!')
        else:
            print('Failed to send email')
    # 번역된 내용을 브라우저로 응답한다.            
    return {"subject":subject,"message":message,"recipient_email":recipient_email}


@routes_bp.get('/movie')
def movie_form():
    #1~25 [1,2,3,4,....,25]
    filenames = [i for i in range(1,26)]
    return render_template('movie.html',filenames=filenames)


@routes_bp.post('/movie')
def movie_proc():
    data = request.json
    # "0,1,1,1,0, ......"
    movie = data['movie']
    #["0","1","1","1",...,"0"]
    movie = movie.split(',')
    # movie 배열의 요소를 정수로 변경하여 list로 변경
    # map: 배열의 요소에 함수를 적용하는 기능을 함.
  
    movie = list(map(int,movie)) #[1,0,1,......]
    
    movies = ['반지의 제왕', 'A Quiet Place (2018)', '러브액츄얼리', '화이트 칙스', 'Interstellar (2014)',
            '해리포터와 마법사의 돌', 'The Autopsy of Jane Doe (2016)', '타이타닉', '세 얼간이', 'A.I. (2001)',
            '캐리비안의 해적', 'The Conjuring (2013)', '맘마미아', '덤 앤 더머', 'The Martian (2015)',
            '닥터 스트레인지', 'The Exorcist (1973)', 'La La Land (2016)', '우리는 동물원을 샀다.', 'Edge of Tomorrow (2014)',
            '아바타 (2009)', 'The Rite (2011)', '비긴 어게인', '미트 페어런츠', 'Gravity (2013)']
    #movie=[1,1,1,0,1,1,....]
    watch = [] # 선택된 영화명이 저장된다.
    for index in range(len(movie)):# 0 ~ 24
        if movie[index] == 1:# 시청한 영화이면
            watch.append(movies[index])# 시청한 영화의 이름을 추가
       
    watch_join = ','.join(watch) # 시청한 영화를 ","로 구분
    
    print('-> watch_join:', watch_join)
    # return watch_join  # 콰이어트 플레이스,제인도,컨저링,엑소시스트,더 라이트

    prompt = f'내가 시청한 영화는 [{watch_join}]이야, 내가 시청한 장르의 영화 중 2000년 이후에 출시되고, 내가 시청하지 않고 평점이 높은 영화 5편을 추천해줘.'
    print('-> prompt:', prompt)
    
    format = '''{"res":"영화 목록"}'''
    # 코딩하기
    response = tool.answer('너는 영화 추천 시스템이야',prompt,format)
    print('-> response:', response)
    
    return response  # json 객체 전달

@routes_bp.get("/fileupload") 
def fileupload_form():
    return render_template("fileupload.html")

@routes_bp.post("/fileupload") 
def fileupload_proc():  
    time.sleep(3) #3초 중지
    # 업로드된 파일 받기(하나만받는다)
    f = request.files['file']
    # 파일사이즈 확인
    file_size = len(f.read())
    # 파일 포인터를 처음으로 이동
    f.seek(0)
    if fileupload.allowed_size(file_size) == False:
        resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다." + str(file_size/1024/1024) + ' M'})  # dict -> json string
        resp.status_code = 500 # 서버 에러
    
    # # 허용 가능한 파일 확장자인지 확인
    if f and fileupload.allowed_file(f.filename):
        # 저장할 경로 지정 (예: 'storage' 폴더에 저장)
        upload_folder = 'storage'
        if not os.path.exists(upload_folder):
          os.makedirs(upload_folder)
        # 파일저장
        f.save(os.path.join(upload_folder,f.filename))
        # dict -> json string
        resp = jsonify({'message':'파일을 저장했습니다.'})
    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})  # dict -> json string
        # resp.status_code = 500 # 서버 에러
        
    return resp

@routes_bp.get("/pdf_text") 
def pdf_text_form():
    return render_template("pdf_text.html")

@routes_bp.post("/pdf_text") 
def pdf_text_proc():  
    time.sleep(3) #3초 중지
    # 업로드된 파일 받기(하나만받는다)
    f = request.files['file']
    # 파일사이즈 확인
    file_size = len(f.read())
    # 파일 포인터를 처음으로 이동
    f.seek(0)
    if fileupload.allowed_size(file_size) == False:
        resp = jsonify({'message': "파일 사이즈가 25M를 넘습니다." + str(file_size/1024/1024) + ' M'})  # dict -> json string
        resp.status_code = 500 # 서버 에러
    
    # # 허용 가능한 파일 확장자인지 확인
    if f and fileupload.allowed_file(f.filename):
        # 저장할 경로 지정 (예: 'static/pdf' 폴더에 저장)
        upload_folder = os.path.join(os.getcwd(),'static','pdf')
        if not os.path.exists(upload_folder):
          os.makedirs(upload_folder)
        # 파일저장
        f.save(os.path.join(upload_folder,f.filename))
        
        # 업로드된 파일경우 
        file_path = os.path.join(upload_folder,f.filename)
        # 업로드된 pdf 파일을 본문만 읽어서 txt파일로 저장
        file = fileupload.pdf_to_text(file_path)
        # txt파일을 읽어서 요약한 결과 받기(llm)
        summary = fileupload.summarize_txt(file)
        
        resp = jsonify({'summary':summary})
        f.close()
    else:
        resp = jsonify({'message': '전송 할 수 없는 파일 형식입니다.'})  # dict -> json string
        # resp.status_code = 500 # 서버 에러
        
    return resp


    