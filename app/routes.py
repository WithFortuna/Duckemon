#routes는 Controller와 유사함
from flask import Blueprint, render_template, request,redirect, url_for
import app.apiNetworking as apiNetworking
from app.parser import *
from app.constants import *
import pokebase #pokeAPI의 wrapper라이브러리. pokebase/api.py - get_data, get_sprite
main = Blueprint('main', __name__)
POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/{id}'


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
    info = get_seasons()[str(season_id)]
    for key, value in info.items():
        if value['rule'] == int(rule):
            season_key = key
            info = info.get(season_key)
    return render_template('show_season_info.html', info = info)

#최다빈도 포켓몬. 상세 보여주기
@main.route('/most_pokemon', methods=['GET', 'POST'])
def most_pokemon():
    if request.method == 'POST':
        return redirect(url_for('main.show_most_pokemon', season_id=request.form['season'], rule=request.form['rule'], ranking=request.form['ranking'], component=request.form['component']))

    return render_template('most_pokemon_form.html')

@main.route('/most_pokemon/details') #input: season_id, rule, ranking, component
def show_most_pokemon():
    season_id = request.args.get('season_id')
    rule = request.args.get('rule')
    ranking = int(request.args.get('ranking'))
    component = request.args.get('component')

    season=apiNetworking.get_seasons()[season_id]
    for key, value in season.items():
        if value['rule'] == int(rule): #싱글매치 또는 더블매치 중 1
            match_id=key
            pokemon = apiNetworking.get_pokemon_rank(value)[ranking-1]
            pokemon_name=POKEMON_NAME[int(pokemon['id'])]
            detail = apiNetworking.get_pokemon_details(season[match_id])[str(pokemon['id'])][str(pokemon['form'])] #detail : 기술, 특성, 도구,배틀팀, 이긴 포켓몬... 모두 포함

            if '기술' in component:
                skills = detail['temoti']['waza']
                for i in range(len(skills)):
                    print("==========================",i,"====================")
                    skills[i]['name'] = SKILL_NAME[int(skills[i]['id'])]
                    skills[i]['index']=i+1
                print("=====================================",skills,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='기술', details=skills, pokemon_name=pokemon_name)

            if '특성' in component:
                abilities = detail['temoti']['tokusei']
                for i in range(len(abilities)):
                    abilities[i]['name'] = ABILITY_NAME[int(abilities[i]['id'])]
                    abilities[i]['index']=i+1
                print("=====================================",abilities,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='특성', details=abilities, pokemon_name=pokemon_name)

            if '도구' in component:
                items=detail['temoti']['motimono']
                for i in range(len(items)):
                    items[i]['name']=ITEM_NAME[int(items[i]['id'])]
                    items[i]['index']=i+1
                print("=====================================",items,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='도구', details=items, pokemon_name=pokemon_name)


            if '배틀팀' in component:
                members=detail['temoti']['pokemon']
                for i in range(len(members)):
                    members[i]['name']=POKEMON_NAME[int(members[i]['id'])]
                    members[i]['index']=i+1
                    members[i]['type'] = POKEMON_TYPE[members[i]['id']][members[i]['form']]
                    members[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in members[i]['type']])

                print("=====================================",members,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='배틀팀', details=members, pokemon_name=pokemon_name)
            if '이긴 포켓몬' in component:
                win_pokemons=detail['win']['pokemon']
                for i in range(len(win_pokemons)):
                    win_pokemons[i]['name']=POKEMON_NAME[int(win_pokemons[i]['id'])]
                    win_pokemons[i]['index']=i+1
                    win_pokemons[i]['type']=POKEMON_TYPE[win_pokemons[i]['id']][win_pokemons[i]['form']]
                    win_pokemons[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in win_pokemons[i]['type']])

                print("=====================================",win_pokemons,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='이긴 포켓몬', details=win_pokemons, pokemon_name=pokemon_name)

            if '이긴 기술' in component:
                win_skills=detail['win']['waza']
                for i in range(len(win_skills)):
                    win_skills[i]['name']=SKILL_NAME[int(win_skills[i]['id'])]
                    win_skills[i]['index']=i+1
                print("=====================================",win_skills,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='이긴 기술', details=win_skills, pokemon_name=pokemon_name)

            if '진 포켓몬' in component:
                lose_pokemons = detail['lose']['pokemon']
                for i in range(len(lose_pokemons)):
                    lose_pokemons[i]['name'] = POKEMON_NAME[int(lose_pokemons[i]['id'])]
                    lose_pokemons[i]['index'] = i + 1
                    lose_pokemons[i]['type'] = POKEMON_TYPE[lose_pokemons[i]['id']][lose_pokemons[i]['form']]
                    lose_pokemons[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in lose_pokemons[i]['type']])

                print("=====================================",lose_pokemons,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='진 포켓몬', details=lose_pokemons, pokemon_name=pokemon_name)

            if '진 기술' in component:
                lose_skills=detail['lose']['waza']
                for i in range(len(lose_skills)):
                    lose_skills[i]['name'] = SKILL_NAME[int(lose_skills[i]['id'])]
                    lose_skills[i]['index'] = i + 1
                print("=====================================",lose_skills,"===================================")
                return render_template('show_most_pokemon_details.html', detail_name ='진 기술', details=lose_skills, pokemon_name=pokemon_name)

@main.route('/pokedex')
def apiPractice(id): #id: str
    URL = POKE_API_URL.format(id = str(id))

    response = requests.get(URL)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"error: {response.status_code}")
    print(response.text)




