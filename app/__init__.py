
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates')
    # app.config.from_object('config.Config')

    # 라우트 불러오기
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

