from flask import Blueprint
from flask import render_template

# Flask Blueprint는 Flask 애플리케이션을 기능 단위로 분리·구조화하기 위한 모듈화 도구
routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/') # http://localhost:5000/
def index():
    return render_template('summary.html')

@routes_bp.route('/hello') # http://localhost:5000/hello
def hello():
    return render_template('hello.html')

@routes_bp.route('/trans')
def trans():
    return render_template('translator.html')

@routes_bp.route('/mail')
def mail():
    return render_template('mail.html')

@routes_bp.route('/file')
def file():
    return render_template('fileupload.html')