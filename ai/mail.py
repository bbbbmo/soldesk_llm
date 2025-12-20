import tool
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

# Gmail SMTP 서버 설정
SENDER_EMAIL = "byungjunmoon6@gmail.com"
SENDER_PASSWORD = 'nqmz wjgp siia wtts'  # Gmail 앱 비밀번호 또는 2단계 인증 시 생성한 비밀번호 사용

# 텍스트가 한글인지 확인하는 함수, re는 정규 표현식을 사용하기 위한 모듈
def is_korean(text):
    return bool(re.search("[가-힣]", text))


def send_email_test():  
    from_addr = SENDER_EMAIL
    to_addr = 'byungjunmoon6@gmail.com'
 
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
 
    server.login(from_addr, 'nqmz wjgp siia wtts')
 
    body = MIMEMultipart()
    body['subject'] = "Python mail 전송 test"
    body['From'] = from_addr
    body['To'] = to_addr
 
    html   = "<div>"
    html += "  GDP 정보와 금융 동향 발표자료를 보냅니다.<br>"
    html += "  <img src='https://i.namu.wiki/i/yLuwE5PCFLWOHW7G91sC72pqv8JXM7jnlWXO9YogEMZvS-QqS47dnmmq2JVLYUj8mzObOByNkIUm96wS0St1lg.webp' style='width: 50%;'>" # 이미지 전송시 절대 경로
    html += "  <br><br>"
    html += "  <a href='http://www.lectureblue.pe.kr/GDP.zip'>발표 자료 다운로드</a>" 
    html += "</div>"
    msg = MIMEText(html, 'html')
    body.attach(msg)
 
    server.sendmail(from_addr=from_addr,
                        to_addrs=[to_addr],  # list, str 둘 다 가능
                        msg=body.as_string())
 
    server.quit()
    print('메일을 발송했습니다.')
    
# 이메일 전송 함수
def send_email(subject, recipient_email, message):
    # MIMEMultipart 객체 생성
    # 여러개의 MIME(Message Internet Mail Extensions) 형식을 포함한 이메일을 만들 때 사용
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    # # 이메일 본문을 번역된 텍스트로 추가
    msg.attach(MIMEText(message, "html"))

    # SMTP 서버에 연결하여 이메일 전송
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()  # TLS 사용
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # 로그인
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())  # 이메일 전송
        print("Email sent successfully with translated content!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()


# 번역을 위한 GPT API 사용
def use_api(msg):
    if is_korean(msg):
        language = '영어'
    else:
        language = '한국어'
    
    prompt = f'아래 문장을 {language}로 번역해줘.\n{msg}'
    format = '''
    {
        "res" : "번역된 문장"
    }
    '''
    response = tool.answer('너는 번역기야',prompt,format)
    
    return response['res']
