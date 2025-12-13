import smtplib

from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText

def send_email():  
    from_addr = 'byungjunmoon6@gmail.com'
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
    