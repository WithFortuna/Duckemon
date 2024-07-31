# !git clone https://github.com/bombedhair/Pokemon-Rank-Parser.git rankparser
import sys
# sys.path.append('/content/rankparser')
from app.constants import *
from app.parser import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
from IPython.display import set_matplotlib_formats
from IPython.display import display, HTML

# 나눔글꼴 설치 경로를 지정합니다.
font_path = 'C:/Users/NT551XCJ/Desktop/start_backend/Project/font/MapleBold.ttf'

# 폰트를 추가하고, 기본 폰트로 설정합니다.
font_entry = fm.FontEntry(fname=font_path, name='NanumGothic')
fm.fontManager.ttflist.insert(0, font_entry)
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothic'})

#
# # 간단한 그래프를 생성하고 표시합니다.
# plt.plot([1, 2, 3], [4, 5, 6])
# plt.title('테스트 플롯')
# plt.show()
from IPython.core.display import HTML
from datetime import datetime
from functools import reduce







# 해당 시즌의 기본 정보를 보여주는 함수입니다.
def display_season_data(num):

    season = get_seasons()[str(num)]
    for match_id in sorted(season.keys()):
        match = season[match_id]
        battle_prefix = '싱글' if match['rule'] == 0 else '더블' # 0 -> 싱글, 1 -> 더블
        display(HTML(f"<h3>시즌 {num} {battle_prefix} 배틀 정보</h3>"))
        print("시즌 이름:", match['name'])
        print("시즌 시작:", match['start'])
        print("시즌 종료:", match['end'])
        print("참여자 수:", match['cnt'])
        print("플레이어 순위 집계 기준:", datetime.fromtimestamp(match['ts1']).strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))
        print("포켓몬 순위 집계 기준:", datetime.fromtimestamp(match['ts2']).strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))

# 원하는 시즌의 싱글 또는 더블배틀 트레이너 순위를 원하는 만큼 보여주는 함수입니다.
def display_trainer_data(season, single, start, end):
    the_season = get_seasons()[str(season)]

    battle_prefix = '싱글' if single else '더블'
    for rule_id in sorted(the_season.keys()):
        rule = '싱글' if rule_id.endswith('1') else '더블'
        if battle_prefix is rule:

            display(HTML(f"<h3>시즌 {season} {rule} 배틀 {start}위 ~ {end}위 플레이어</h3>"))
            trainers = get_trainer_rank(the_season[rule_id], start // 1000 + 1)
            if start // 1000 != end // 1000:
                trainers2 = get_trainer_rank(the_season[rule_id], end // 1000 + 1)
                trainers += trainers2

            dataframe = (pd.DataFrame(trainers[start%1000-1:(end%1000 if (start//1000 == end//1000) else end%1000+1000)])
                           .drop(columns=['icon', 'lng'])
                           .rename(columns={'name': '트레이너', 'rank': '순위', 'rating_value': '레이팅'})
                           .set_index('순위'))
            display(dataframe)

# 원하는 시즌의 특정 레이팅 점수 커트라인 등수를 보여주는 함수입니다.
def display_rating_cutline(season, single, rating):
    the_season = get_seasons()[str(season)]

    battle_prefix = '싱글' if single else '더블'
    for rule_id in sorted(the_season.keys()):
        rule = '싱글' if rule_id.endswith('1') else '더블'
        if battle_prefix is rule:

            cutline = 0
            while cutline % 1000 == 0:
                cutline += 1000
                trainers = get_trainer_rank(the_season[rule_id], cutline // 1000)
                for i in range(1000):
                    if int(trainers[i]['rating_value']) < rating * 1000:
                        cutline -= 1000 - i
                        break

            display(HTML(f"<h3>시즌 {season} {rule} 배틀 {rating}점 커트라인은 {cutline}위입니다.</h3>"))
            start = cutline - 6 if cutline >= 6 else 0
            end = cutline + 4
            trainers = get_trainer_rank(the_season[rule_id], start // 1000 + 1)
            if start // 1000 != end // 1000:
                trainers2 = get_trainer_rank(the_season[rule_id], end // 1000 + 1)
                trainers += trainers2
            dataframe = (pd.DataFrame(trainers[start%1000:(end%1000 if (start//1000 == end//1000) else end%1000+1000)])
                           .drop(columns=['icon', 'lng'])
                           .rename(columns={'name': '트레이너', 'rank': '순위', 'rating_value': '레이팅'})
                           .set_index('순위'))
            display(dataframe)

# 원하는 시즌의 싱글 또는 더블배틀 포켓몬 빈도 순위를 원하는 만큼 보여주는 함수입니다.
def display_pokemon_usage(season, single, start, end):
    the_season = get_seasons()[str(season)]

    battle_prefix = '싱글' if single else '더블'
    for rule_id in sorted(the_season.keys()):
        rule = '싱글' if rule_id.endswith('1') else '더블'
        if battle_prefix is rule:

            display(HTML(f"<h3>시즌 {season} {rule} 배틀 빈도 {start}위 ~ {end}위 포켓몬</h3>"))
            pokemons = get_pokemon_rank(the_season[rule_id])
            for i in range(start - 1, end):
                pokemons[i]['name'] = POKEMON_NAME[pokemons[i]['id']]
                pokemons[i]['type'] = POKEMON_TYPE[pokemons[i]['id']][pokemons[i]['form']]
                pokemons[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in pokemons[i]['type']])
                pokemons[i]['ranking'] = i + 1

            dataframe = (pd.DataFrame(pokemons[start-1:end])
                           .drop(columns=['form', 'id', 'type'])
                           .rename(columns={'ranking': '순위', 'name': '이름', 'type_kor': '타입'})
                           .set_index('순위'))
            display(dataframe)

# 원하는 포켓몬의 상세 정보를 보여주는 함수입니다.
def display_pokemon_data(season, single, ranking, components):
  while True:
    if season ==21:
      break
    else:
      while True:
        if ranking ==10:
          break
        else:
          the_season = get_seasons()[str(season)]

          battle_prefix = '싱글' if single else '더블'
          for rule_id in sorted(the_season.keys()):
              rule = '싱글' if rule_id.endswith('1') else '더블'
              if battle_prefix is rule:

                  display(HTML(f"<h3>시즌 {season} {rule} 배틀 빈도 {ranking}위 포켓몬 상세 정보</h3>"))
                  pokemon = get_pokemon_rank(the_season[rule_id])[ranking - 1]
                  print("이름:", POKEMON_NAME[pokemon['id']])
                  print("타입:", ', '.join([TYPE_NAME[x] for x in POKEMON_TYPE[pokemon['id']][pokemon['form']]]))

                  details = get_pokemon_details(the_season[rule_id])[str(pokemon['id'])][str(pokemon['form'])]

                  if '기술' in components:
                      moves = details['temoti']['waza']
                      display(HTML('<h4>기술</h4>'))
                      for i in range(0, len(moves)):
                          moves[i]['name'] = SKILL_NAME[int(moves[i]['id'])]
                          moves[i]['ranking'] = i + 1
                      moves_df = (pd.DataFrame(moves)
                                    .drop(columns=['id'])
                                    .rename(columns={'name': '이름', 'ranking': '순위', 'val': '빈도'})
                                    .set_index('순위'))
                      display(moves_df)

                  if '특성' in components:
                      abilities = details['temoti']['tokusei']
                      display(HTML('<h4>특성</h4>'))
                      for i in range(0, len(abilities)):
                          abilities[i]['name'] = ABILITY_NAME[int(abilities[i]['id'])]
                          abilities[i]['ranking'] = i + 1
                      abilities_df = (pd.DataFrame(abilities)
                                    .drop(columns=['id'])
                                    .rename(columns={'name': '이름', 'ranking': '순위', 'val': '빈도'})
                                    .set_index('순위'))
                      display(abilities_df)

                  if '도구' in components:
                      items = details['temoti']['motimono']
                      display(HTML('<h4>도구</h4>'))
                      for i in range(0, len(items)):
                          items[i]['name'] = ITEM_NAME[int(items[i]['id'])]
                          items[i]['ranking'] = i + 1
                      items_df = (pd.DataFrame(items)
                                    .drop(columns=['id'])
                                    .rename(columns={'name': '이름', 'ranking': '순위', 'val': '빈도'})
                                    .set_index('순위'))
                      display(items_df)

                  if '배틀팀' in components:
                      parties = details['temoti']['pokemon']
                      display(HTML('<h4>함께 배틀팀에 포함된 포켓몬 TOP 10</h4>'))
                      for i in range(0, len(parties)):
                          parties[i]['name'] = POKEMON_NAME[parties[i]['id']]
                          parties[i]['type'] = POKEMON_TYPE[parties[i]['id']][parties[i]['form']]
                          parties[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in parties[i]['type']])
                          parties[i]['ranking'] = i + 1
                      parties_df = (pd.DataFrame(parties)
                                    .drop(columns=['form', 'id', 'type'])
                                    .rename(columns={'ranking': '순위', 'name': '이름', 'type_kor': '타입'})
                                    .set_index('순위'))
                      display(parties_df)

                      #parties_df.to_csv('parties_df.csv', index=False, encoding='utf-8-sig')
                      #from google.colab import files
                      #files.download('parties_df.csv')

                  if '이긴 포켓몬' in components:
                      win_pokemons = details['win']['pokemon']
                      display(HTML('<h4>이 포켓몬이 쓰러뜨린 포켓몬 TOP 10</h4>'))
                      for i in range(0, len(win_pokemons)):
                          win_pokemons[i]['name'] = POKEMON_NAME[win_pokemons[i]['id']]
                          win_pokemons[i]['type'] = POKEMON_TYPE[win_pokemons[i]['id']][win_pokemons[i]['form']]
                          win_pokemons[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in win_pokemons[i]['type']])
                          win_pokemons[i]['ranking'] = i + 1
                      win_pokemons_df = (pd.DataFrame(win_pokemons)
                                    .drop(columns=['form', 'id', 'type'])
                                    .rename(columns={'ranking': '순위', 'name': '이름', 'type_kor': '타입'})
                                    .set_index('순위'))
                      display(win_pokemons_df)

                  if '이긴 기술' in components:
                      win_moves = details['win']['waza']
                      display(HTML('<h4>이 포켓몬이 상대를 쓰러뜨릴 때 사용한 기술 TOP 10</h4>'))
                      for i in range(0, len(win_moves)):
                          win_moves[i]['name'] = SKILL_NAME[int(win_moves[i]['id'])]
                          win_moves[i]['ranking'] = i + 1
                      win_moves_df = (pd.DataFrame(win_moves)
                                    .drop(columns=['id'])
                                    .rename(columns={'name': '이름', 'ranking': '순위', 'val': '빈도'})
                                    .set_index('순위'))
                      display(win_moves_df)

                  if '진 포켓몬' in components:
                      lose_pokemons = details['lose']['pokemon']
                      display(HTML('<h4>이 포켓몬을 쓰러뜨린 포켓몬 TOP 10</h4>'))
                      for i in range(0, len(lose_pokemons)):
                          lose_pokemons[i]['name'] = POKEMON_NAME[lose_pokemons[i]['id']]
                          lose_pokemons[i]['type'] = POKEMON_TYPE[lose_pokemons[i]['id']][lose_pokemons[i]['form']]
                          lose_pokemons[i]['type_kor'] = ', '.join([TYPE_NAME[x] for x in lose_pokemons[i]['type']])
                          lose_pokemons[i]['ranking'] = i + 1
                      lose_pokemons_df = (pd.DataFrame(lose_pokemons)
                                    .drop(columns=['form', 'id', 'type'])
                                    .rename(columns={'ranking': '순위', 'name': '이름', 'type_kor': '타입'})
                                    .set_index('순위'))
                      display(lose_pokemons_df)

                  if '진 기술' in components:
                      lose_moves = details['lose']['waza']
                      display(HTML('<h4>이 포켓몬을 쓰러뜨린 기술 TOP 10</h4>'))
                      for i in range(0, len(lose_moves)):
                          lose_moves[i]['name'] = SKILL_NAME[int(lose_moves[i]['id'])]
                          lose_moves[i]['ranking'] = i + 1
                      lose_moves_df = (pd.DataFrame(lose_moves)
                                    .drop(columns=['id'])
                                    .rename(columns={'name': '이름', 'ranking': '순위', 'val': '빈도'})
                                    .set_index('순위'))
                      display(lose_moves_df)
          season+=1
          continue
      continue



def track_pokemon_data(pokemon, form, single, seasons, top_N, components, graphics):
    for pokemon_id, name in POKEMON_NAME.items():
        if pokemon == name:
            dex_no = pokemon_id

    battle_prefix = '싱글' if single else '더블'
    display(HTML(f"<h3>시즌별 {battle_prefix} 배틀 {pokemon} 상세 정보</h3>"))
    print("타입:", ', '.join([TYPE_NAME[x] for x in POKEMON_TYPE[dex_no][form]]))

    moves_df = {}
    abilities_df = {}
    items_df = {}
    win_moves_df = {}
    lose_moves_df = {}

    the_seasons = get_seasons()
    columns = ['이름']
    for season in seasons:
        columns.append(f'시즌{season}')

        for rule_id in sorted(the_seasons[str(season)].keys()):
            rule = '싱글' if rule_id.endswith('1') else '더블'
            if battle_prefix is rule:

                details = get_pokemon_details(the_seasons[str(season)][rule_id])[str(dex_no)][str(form)]

                if '기술' in components:
                    moves = details['temoti']['waza']
                    for i in range(0, len(moves)):
                        moves[i]['name'] = SKILL_NAME[int(moves[i]['id'])]
                        moves[i]['ranking'] = i + 1
                    moves_df[season] = (pd.DataFrame(moves)
                                  .drop(columns=['id'])
                                  .rename(columns={'name': '이름', 'ranking': '순위', 'val': f'시즌{season}'})
                                  .set_index('순위')
                                  .astype({f'시즌{season}': 'float64'}))

                if '특성' in components:
                    abilities = details['temoti']['tokusei']
                    for i in range(0, len(abilities)):
                        abilities[i]['name'] = ABILITY_NAME[int(abilities[i]['id'])]
                        abilities[i]['ranking'] = i + 1
                    abilities_df[season] = (pd.DataFrame(abilities)
                                  .drop(columns=['id'])
                                  .rename(columns={'name': '이름', 'ranking': '순위', 'val': f'시즌{season}'})
                                  .set_index('순위')
                                  .astype({f'시즌{season}': 'float64'}))

                if '도구' in components:
                    items = details['temoti']['motimono']
                    for i in range(0, len(items)):
                        items[i]['name'] = ITEM_NAME[int(items[i]['id'])]
                        items[i]['ranking'] = i + 1
                    items_df[season] = (pd.DataFrame(items)
                                  .drop(columns=['id'])
                                  .rename(columns={'name': '이름', 'ranking': '순위', 'val': f'시즌{season}'})
                                  .set_index('순위')
                                  .astype({f'시즌{season}': 'float64'}))

    if '기술' in components:
        display(HTML('<h4>기술</h4>'))
        moves_df_merged = (reduce(lambda left, right: pd.merge(left, right, on='이름', how='outer'),
                                 moves_df.values())
                           .sort_values(by=f'시즌{max(seasons)}', ascending=False)
                           .reset_index(drop=True)[:top_N][columns])
        if '표' in graphics:
            moves_df_merged.index += 1
            display(moves_df_merged)
        if '그래프' in graphics:
            moves_df_merged = moves_df_merged.set_index('이름').T
            plt.figure(figsize=[15, 7])
            sns.lineplot(data=moves_df_merged, marker="o", dashes=False, sort=False)
            plt.ylabel('빈도(%)')
            plt.legend(fontsize=12, bbox_to_anchor=(1, 0.5), loc='center left')
            plt.show()

    if '특성' in components:
        display(HTML('<h4>특성</h4>'))
        abilities_df_merged = (reduce(lambda left, right: pd.merge(left, right, on='이름', how='outer').fillna(0),
                                 abilities_df.values())
                               .sort_values(by=f'시즌{max(seasons)}', ascending=False)
                               .reset_index(drop=True)[columns])
        if '표' in graphics:
            abilities_df_merged.index += 1
            display(abilities_df_merged)
        if '그래프' in graphics:
            abilities_df_merged = abilities_df_merged.set_index('이름').T
            plt.figure(figsize=[15, 7])
            sns.lineplot(data=abilities_df_merged, marker="o", dashes=False, sort=False)
            plt.ylabel('빈도(%)')
            plt.legend(fontsize=12, bbox_to_anchor=(1, 0.5), loc='center left')
            plt.show()

    if '도구' in components:
        display(HTML('<h4>도구</h4>'))
        items_df_merged = (reduce(lambda left, right: pd.merge(left, right, on='이름', how='outer'),
                                 items_df.values())
                           .sort_values(by=f'시즌{max(seasons)}', ascending=False)
                           .reset_index(drop=True)[:top_N][columns])
        if '표' in graphics:
            items_df_merged.index += 1
            display(items_df_merged)
        if '그래프' in graphics:
            items_df_merged = items_df_merged.set_index('이름').T
            plt.figure(figsize=[15, 7])
            sns.lineplot(data=items_df_merged, marker="o", dashes=False, sort=False)
            plt.ylabel('빈도(%)')
            plt.legend(fontsize=12, bbox_to_anchor=(1, 0.5), loc='center left')
            plt.show()