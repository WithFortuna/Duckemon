#routes는 Controller와 유사함
import traceback

from flask import Blueprint, render_template, request,redirect, url_for, send_from_directory
import app.apiNetworking as apiNetworking
from app.parser import *
from app.constants import *
import pokebase, pokebase.api, pokebase.loaders #pokeAPI의 wrapper라이브러리. pokebase/api.py - get_data, get_sprite
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

main = Blueprint('main', __name__)
POKE_API_URL = 'https://pokeapi.co/api/v2/{endpoint}/{id}'


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


#------------------------------------------------------ 하단의 함수들은 모두 pokeAPI를 이용
@main.route('/pokedexAlpha')
def apiPractice(id): #id: str
    URL = POKE_API_URL.format(id = str(id))

    response = requests.get(URL)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"error: {response.status_code}")
    print(response.text)

@main.route('/cacheFile/sprite/pokemon/<filename>')
def get_pokemon_sprite(filename):
    # pokemon_obj = pokebase.pokemon(filename)
    #
    # filename = str(pokemon_obj.id)+'.png' #pokemon_name->pokemon_id 변환
    with open('pokemons_ver2.json', 'r', encoding='utf-8') as json_file:
        pokemons = json.load(json_file)
    pokemon = next((p for p in pokemons if p.get('name') == filename), None)
    id = pokemon['url'].split('/')[-2]
    print(f"위치: get_pokemon_sprite 포켓몬: {pokemon} 이미지 로드, id: {id}")


    #send_from_directroy 사용예시
    #경로: C:/Users/NT551XCJ/Desktop/start_backend/Project/Duckemon/cacheFile/sprite/pokemon/1.png
    #send_from_directroy('C:/Users/NT551XCJ/Desktop/start_backend/Project/Duckemon/cacheFile/sprite/pokemon', 1.png)
    filename = id+'.png'
    return send_from_directory('C:/Users/NT551XCJ/Desktop/start_backend/Project/Duckemon/cacheFile/sprite/pokemon', filename)
#실시간 pokeAPI데이터가 아닌 로컬에 저장되어 있는 pokemons.json파일을 이용
@main.route('/pokedex')
def pokedex_home():
    #도감화면
    #필요 데이터: 포켓몬 객체
    #포켓몬 객체 = {이름, ability, form, type }
    #전달인자: pokemons리스트

    with open('pokemons_ver2.json', 'r', encoding='utf-8') as json_file:
        all_pokemons = json.load(json_file)


    page = int(request.args.get('page', 1))  # 페이지 번호, 기본값은 1
    per_page = 30  # 한 페이지에 표시할 포켓몬 수
    start = (page - 1) * per_page
    end = start + per_page
    pokemons = all_pokemons[start:end]  # 현재 페이지에 해당하는 포켓몬들 선택

    total_pages = (len(all_pokemons) + per_page - 1) // per_page  # 전체 페이지 수 계산

    return render_template('show_pokedex.html', pokemons=pokemons, page=page, total_pages=total_pages)


@main.route('/pokedex/<pokemon_name>')
def pokedex_detail(pokemon_name):
    #pokemon fetch
    with open('pokemons_ver2.json', 'r', encoding='utf-8') as json_file:
        pokemons = json.load(json_file)
    pokemon = next((p for p in pokemons if p.get('name') == pokemon_name),None)
    print(f"pokemon_name: {pokemon_name}, pokemon: {pokemon}")
    try:
        if pokemon is None:
            raise ValueError("포켓몬 못찾음")
    except ValueError as e:
        print(f"오류발생: {e}")

    return render_template('show_pokedex_detail.html', pokemon = pokemon)



#기능: pokemons.json 파일을 초기화 by pokeAPI서버.
def init_pokedex(start, end): # pokemons[start] ~ pokemons[end-1] 까지 api서 정보 받아오기 및 업데이트

    pokemons = pokebase.api.get_data('pokemon')['results']
    with open('pokemons.json', 'r', encoding='utf-8') as json_file:
        old_pokemons = json.load(json_file)

    ## old_pokemons와 새로 업데이트한 pokemons비교 하기 전
    #pokemons 새로 받아오기#################################################################

# j=0
    for k in range(start, end): # pokemons[start] ~ pokemons[end-1] 까지 api서 정보 받아오기
        # j+=1
        # if j==10:
        #     break
        pokemon= pokemons[k]
        name = pokemon['name']
        pokemon_obj = pokebase.loaders.pokemon(name)
        # print(f"없는 포켓몬 추가 & 이름: {name}")

        abilities = pokemon_obj.abilities
        ability_list = []
        is_hidden_list = []
        for ability in abilities:
            names = ability.ability.names
            for lan_name in names:
                if lan_name.language.name == 'ko':
                    ability_list.append(lan_name.name)
                    # print("------------------",lan_name.name)
            is_hidden_list.append(ability.is_hidden)
        pokemon['ability'] = ability_list
        pokemon['is_hidden'] = is_hidden_list
        # print("**포켓몬: ",pokemon)

        # 2. forms/name 추가
        forms = pokemon_obj.forms
        form_list = []
        for form in forms:
            print(form.id_)
            form_list.append(pokebase.loaders.pokemon_form(form.id_).name)
        pokemon['form'] = form_list

        # 3. types/type/name 추가
        types = pokemon_obj.types
        type_list = []
        for type in types:
            type_list.append(type.type.name)
        pokemon['type'] = type_list

        # 4. sprites/front-default의 systemPath 추가
        sprite = pokebase.loaders.sprite('pokemon', pokemon_obj.id) #**kwargs 지정을 안했으므로 front_default선택
        pokemon['sprite'] = sprite.path
    print('*************초기화 완료************', pokemons,"***************")

        ######################################################################## 하단은 old_pokemon과pokemons비교 및 업데이트
    updated1 = False
    # size=0 #업데이트 예정 포켓몬 개수
    for n in range(start,end):
        pokemon= pokemons[n]
        name = pokemon['name']
        updated2 = False
        # size+=1
        # if size==8:
        #     print("종료")
        #     break

        result = next((temp for temp in old_pokemons if temp['name'] == name), None)
        # case1: pokemons/pokemon/name이 old_pokemons에 없는 경우 : pokemon 추가
        if result is None:
            updated1=True
            updated2=True
            print(f"없는 포켓몬 추가 & 이름: {name}")
            old_pokemons.append(pokemon)

        # case2: pokemon/name은 존재 && 해당 포켓몬의 내용이 old_pokemons에 없는 경우 : 해당 pokemon 부분 수정
        elif not all(result.get(key) == value for key, value in pokemon.items()):
            print(f"존재하는 포켓몬 부분 수정: {name}")
            result.update(pokemon)
            updated1=True
            updated2=True

        if not updated2:
            print(f"포켓몬 {name}은 건너뜀")

    if updated1:
        try:
            with open('pokemons.json', 'w', encoding='utf-8') as json_file:
                json.dump(old_pokemons, json_file, ensure_ascii=False, indent=4)
            print("포켓몬 정보가 성공적으로 저장되었습니다.")
            print("old_pokemons: ",old_pokemons)
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    else:
        print("업데이트할 내용이 없습니다.")
        print("old_pokemons: ", old_pokemons)

    #
    # #1. abilities/ability 및 is_hidden을 pokemon딕셔너리에 추가
    # for pokemon in pokemons:
    #     name=pokemon['name']
    #     pokemon_obj = pokebase.loaders.pokemon(name)
    #     # info = pokebase.api.get_data('pokemon',name) 필요시 name_id_convert(endpoint, name_or_id)
    #     abilities=pokemon_obj.abilities
    #     ability_list = []
    #     is_hidden_list=[]
    #     for ability in abilities:
    #         names = ability.ability.names
    #         for lan_name in names:
    #             if lan_name.language.name == 'ko':
    #                 ability_list.append(lan_name.name)
    #                 # print("------------------",lan_name.name)
    #         is_hidden_list.append(ability.is_hidden)
    #     pokemon['ability'] = ability_list
    #     pokemon['is_hidden'] = is_hidden_list
    #     # print("**포켓몬: ",pokemon)
    #
    #     #2. forms/name 추가
    #     forms=pokemon_obj.forms
    #     form_list=[]
    #     for form in forms:
    #         print(form.id_)
    #         form_list.append(pokebase.loaders.pokemon_form(form.id_).name)
    #     pokemon['form'] = form_list
    #
    #     #3. types/type/name 추가
    #     types=pokemon_obj.types
    #     type_list=[]
    #     for type in types:
    #         type_list.append(type.type.name)
    #     pokemon['type'] = type_list
    #
    #     #4. sprites/front-default의 systemPath 추가
    #     sprite = pokebase.loaders.sprite('pokemon', pokebase.loaders.pokemon(name).id)
    #     pokemon['sprite'] = sprite.path
    #     print('**pokemon:', pokemon)
    #
    #     with open('pokemons.json', 'w', encoding='utf-8') as json_file:
    #         json.dump(pokemons, json_file, ensure_ascii=False, indent=4)
    #

#init_pokedex()개선판: 멀티스레딩
def process_pokemon(pokemon):
    pokemon_obj=None
    try:
        name = pokemon['name']
        pokemon_obj = pokebase.loaders.pokemon(name)
        if pokemon_obj is None:
            raise ValueError(f"객체생성실패1 pokemon: {name}")

        if pokemon_obj is not None:

            # Abilities
            abilities = pokemon_obj.abilities
            ability_list = []
            is_hidden_list = []
            for ability in abilities:
                names = ability.ability.names
                for idx, lan_name in enumerate(names): #index와 name원소 동시에 취함
                    if lan_name.language.name == 'ko':
                        ability_list.append(lan_name.name)
                    elif idx == len(names)-1: #'ko'가 names에 없는 경우를 위해
                        ability_list.append( next((lan_name.name for lan_name in names if lan_name.language.name == 'en'), None) )

                is_hidden_list.append(ability.is_hidden)
            pokemon['ability'] = ability_list
            pokemon['is_hidden'] = is_hidden_list

            # Forms
            forms = pokemon_obj.forms
            form_list = []
            for form in forms:
                print(form.id_)
                form_list.append(pokebase.loaders.pokemon_form(form.id_).name)
            pokemon['form'] = form_list
            # Types
            types = pokemon_obj.types
            type_list = []
            for type in types:
                type_list.append(type.type.name)
            pokemon['type'] = type_list

            # Sprite
            try:
                sprite = pokebase.loaders.sprite('pokemon', pokemon_obj.id)
                pokemon['sprite'] = sprite.path
            except Exception as e:
                pokemon['sprite'] = None
            # time.sleep(0.5)  # API 요청 제한을 고려한 대기 시간
            return pokemon
    except Exception as exc:
        print(f"===========================위치:process_pokemon pokemon: {name}// pokemon_obj:{pokemon_obj} 처리중 오류발생: {exc}")
        traceback.print_exc()
        # time.sleep(1)
        return pokemon

def init_pokedex_enhanced(start, end):
    ##########################################################part1: 데이터 받아오기 & 캐시 및 로컬변수에 저장하기
    pokemons = pokebase.api.get_data('pokemon')['results']
    with open('pokemons_ver2.json', 'r', encoding='utf-8') as json_file:
        old_pokemons = json.load(json_file)

    # 멀티스레딩을 사용하여 병렬 처리
    with ThreadPoolExecutor(max_workers=5) as executor:  # max_workers를 조정하여 동시 요청 수 제한
        future_to_pokemon = {executor.submit(process_pokemon, pokemons[k]): k for k in range(start, end)} #future_to_pokemon = {pokemmons[1]:1, pokemons[2]:2 ,...  }
        for future in as_completed(future_to_pokemon): #future:pokemons[?]. 즉 key
            k = future_to_pokemon[future]
            try:
                pokemon = future.result()
                print(f"처리 완료: {pokemon['name']}")
            except Exception as exc:
                print("==============",pokemons[k],'====================')
                print(f'{pokemons[k]["name"]} 처리 중 오류 발생: {exc}')
                continue

    print('*************초기화 완료************', pokemons[start:end], "***************")
    ##################################################################################################part2: 받아온 새 데이터를 로컬 json파일에 업데이트
    updated1 = False
    # size=0 #업데이트 예정 포켓몬 개수
    for n in range(start,end):
        pokemon= pokemons[n]
        name = pokemon['name']
        updated2 = False
        # size+=1
        # if size==8:
        #     print("종료")
        #     break

        result = next((temp for temp in old_pokemons if temp['name'] == name), None)
        # case1: pokemons/pokemon/name이 old_pokemons에 없는 경우 : pokemon 추가
        if result is None:
            updated1=True
            updated2=True
            print(f"없는 포켓몬 추가 & 이름: {name}")
            old_pokemons.append(pokemon)

        # case2: pokemon/name은 존재 && 해당 포켓몬의 내용이 old_pokemons에 없는 경우 : 해당 pokemon 부분 수정
        elif not all(result.get(key) == value for key, value in pokemon.items()):
            print(f"존재하는 포켓몬 부분 수정: {name}")
            result.update(pokemon)
            updated1=True
            updated2=True

        if not updated2:
            print(f"포켓몬 {name}은 건너뜀")

    if updated1:
        try:
            with open('pokemons_ver2.json', 'w', encoding='utf-8') as json_file:
                json.dump(old_pokemons, json_file, ensure_ascii=False, indent=4)
            print("포켓몬 정보가 성공적으로 저장되었습니다.")
            print("old_pokemons: ",old_pokemons)
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
    else:
        print("업데이트할 내용이 없습니다.")
        print("old_pokemons: ", old_pokemons)

