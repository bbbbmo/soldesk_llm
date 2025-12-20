from flask import Blueprint, request
from flask import render_template
import tool
import mail

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
def mail():
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

@routes_bp.route('/file')
def file():
    return render_template('fileupload.html')