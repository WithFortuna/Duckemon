#routes는 Controller와 유사함
from flask import Blueprint, render_template, request,redirect, url_for
import app.apiNetworking as apiNetworking
from app.constants import *
main = Blueprint('main', __name__)

#url_for(main.A함수명) 에서 main.A는 현재 스크립트의 '함수명'이다.
# => 직접적인 url대신 사용

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')


#최다빈도 포켓몬 보여주기 페이지
@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        season = request.form['season'] # season: value만 나옴
        # 여기에 시즌 데이터를 처리하는 로직을 추가할 수 있습니다.
        return redirect(url_for('main.often_used_pokemon', season_id=season))
    return render_template('search.html')

@main.route('/search/<season_id>')
def often_used_pokemon(season_id):
    pokemons = apiNetworking.display_pokemon_usage(season_id,True,1,10) #수정 필요 : 사용자에게 single,start,end 필드를 입력받아야한다

    return render_template('showOftenUsedPokemon.html', season_id=season_id, pokemons=pokemons)



#시즌 정보 보여주기 페이지
@main.route('/season_info', methods=['GET', 'POST'])
def season_info():
    if request.method == 'POST':
        season = request.form['season']
        rule = request.form['rule']

        return redirect(url_for('main.show_season_info', season_id=season, rule=rule))
    return render_template('season_info_form.html')

@main.route('/season_info/<season_id>/<rule>')
def show_season_info(season_id, rule):
    info = apiNetworking.display_season_data(season_id)
    for key, value in info.items():
        if value['rule'] == int(rule):
            season_key = key
            info = info.get(season_key)
    return render_template('show_season_info.html', info = info)

#최다빈도 포켓몬 상세 보여주기
@main.route('/mostPokemon', methods=['GET', 'POST'])
def most_pokemon():
    if request.method == 'POST':
        return redirect(url_for('main.show_most_pokemon', season_id=request.form['season'], rule=request.form['rule'], ranking=request.form['ranking'], component=request.form['component']))

    return render_template('most_pokemon_form.html')

@main.route('/mostPokemon/details') #input: season_id, rule, ranking, component
def show_most_pokemon():
    season_id = request.args.get('season_id')
    rule = request.args.get('rule')
    ranking = request.args.get('ranking')
    component = request.args.get('component')

    season=apiNetworking.get_seasons()[season_id]
    for key, value in season.items():
        if value['rule'] == int(rule): #싱글매치 또는 더블매치 중 1
            match_id=key
            pokemon = apiNetworking.get_pokemon_rank(value)[ranking-1]
            detail = apiNetworking.get_pokemon_details(season[match_id])[str(pokemon['id'])][str(pokemon['form'])] #detail : 기술, 특성, 도구,배틀팀, 이긴 포켓몬... 모두 포함
            if '기술' in component:
                skills = detail['temoti']['waza']
                for i in range(len(skills)):
                    print("==========================",i,"====================")
                    skills[i]['name'] = SKILL_NAME[int(skills[i]['id'])]
                    skills[i]['index']=i+1

            # if '특성' in component:
            #
            # if '도구' in component:
            # if '배틀팀' in component:
            # if '이긴 포켓몬' in component:
            # if '이긴 기술' in component:
            # if '진 포켓몬' in component:
            # if '진 기술' in component:

            return render_template('most_pokemon_details.html')



