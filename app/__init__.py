
from flask import Flask

POKE_API_URL = 'https://pokeapi.co/api/v2/{endpoint}/{id}'
def create_app():
    app = Flask(__name__, template_folder='../templates')
    # app.config.from_object('config.Config')

    # 라우트 불러오기
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint) #서버와 url맵핑
    #
    # from .init_pokemons import init_pokemons as init_pokemons
    # init_pokemons()
    return app

