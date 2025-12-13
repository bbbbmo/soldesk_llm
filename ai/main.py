from flask import Flask, request
from flask_cors import CORS
from route import routes_bp

app = Flask(__name__)  # __name__ == '__main__'
CORS(app)

app.register_blueprint(routes_bp)

app.run(host="0.0.0.0", port=5000, debug=True) # 0.0.0.0: 어디서나 접속, debug=True: 소스 변경시 자동 재시작
'''
activate ai
python main.py
'''