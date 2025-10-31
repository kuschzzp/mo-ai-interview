from dotenv import load_dotenv
from flask import Flask

from apis.interview_apis import interview_bp
from apis.interview_stream_apis import interview_stream_bp
from handler.error_handlers import register_error_handlers

# 加载 .env
load_dotenv()

app = Flask(__name__)

# ===================注册错误处理器===================
register_error_handlers(app)

# ===================注册接口=========================
app.register_blueprint(interview_bp)
app.register_blueprint(interview_stream_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8910)
