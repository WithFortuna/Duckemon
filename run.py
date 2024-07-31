from app import create_app
from app.routes import main
import app.apiNetworking as apiNetworking

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# apiNetworking.display_season_data(10)

#@title 포켓몬 빈도 순위 확인하기
season = 3 #@param {type:"integer"}
single = True #@param {type:"boolean"}
start = 1 #@param {type:"integer"}
end = 10 #@param {type:"integer"}
# season은 시즌 번호, start는 시작 순위, end는 끝 순위입니다.
# single에 True를 입력하면 싱글배틀 순위를, False를 입력하면 더블배틀 순위를 보여줍니다.
apiNetworking.display_pokemon_usage(season,single,start,end)