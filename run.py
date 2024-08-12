from app import create_app
from app.routes import main
import app.apiNetworking as apiNetworking
import app.routes as routes
import pokebase.cache as cache
import pokebase.api

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) #서버 시작하기
cache.set_cache('C:/Users/NT551XCJ/Desktop/start_backend/Project/Duckemon/cacheFile/') #pokeAPI chace폴더 설정


# apiNetworking.display_season_data(10)

# #@title 포켓몬 빈도 순위 확인하기
# season = 6 #@param {type:"integer"}
# single = True #@param {type:"boolean"}
# start = 1 #@param {type:"integer"}
# end = 10 #@param {type:"integer"}
# season은 시즌 번호, start는 시작 순위, end는 끝 순위입니다.
# single에 True를 입력하면 싱글배틀 순위를, False를 입력하면 더블배틀 순위를 보여줍니다.
#apiNetworking.display_pokemon_usage(season,single,start,end)
# apiNetworking.display_trainer_data(season,single,start,end)
# season = apiNetworking.display_season_data(9)
# print("=======================",season,"=====================")
# apiNetworking.display_season_data(35)
# apiNetworking.display_pokemon_data(season,single,1,'기술')

# routes.apiPractice('1')

#pokebase 호출 예시
#예시1: 함수
# pokebase.api._call_sprite_api('pokemon',11, other=True, official_artwork=True, shiny=True)
# #예시2: 클래스
# p1 = pokebase.SpriteResource('pokemon',11,other=True, official_artwork=True, shiny=True) #SpriteResource 클래스 객체 생성
# print("==================",p1.url, p1.sprite_id, "============================") #객체 멤버변수 호출

# routes.pokedex_home()


#pokeAPI초기화 ver1
#pokemons[99]까지 완료
# pokemons = pokebase.api.get_data('pokemon')['results']
# end=len(pokemons)
# for i in range(0,end):
#     if not (i%50 == 0):
#         continue
#     if i+50>end:
#         routes.init_pokedex(i,end)
#     routes.init_pokedex(i,i+50) #i:50의 배수
#


class CICD:
    def __init__(self, a, b):
        self.a = a  # 멤버 변수 a
        self.b = b  # 멤버 변수 b

    def memberFunction1(self):
        # 예제: 멤버 변수 a와 b의 합을 반환
        return self.a + self.b

    #함수명: update_pokeAPI
    #상황: 공식 포켓몬API의 수정, 변경, 업데이트가 있을 시
    #기능: pokemons_ver2.json파일의 모든 포켓몬에 대해 정보 업데이트
    def update_pokeAPI(self):
        # pokeAPI초기화 ver2
        pokemons = pokebase.api.get_data('pokemon')['results']
        start=0
        end = len(pokemons)  # 총 포켓몬 수: 1302개
        for i in range(start, end):
            if not (i % 50 == 0):
                continue
            if i + 50 > end:
                routes.init_pokedex_enhanced(i, end)
            routes.init_pokedex_enhanced(i, i + 50)  # i:50의 배수

