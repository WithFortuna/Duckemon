import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import svm

def ai_recommend_pokemon(input_pokemons): #input_pokemons: str
    # 데이터 로드 (파일 경로를 수정하세요)
    df = pd.read_csv('C:/Users/NT551XCJ/Desktop/start_backend/Project/Duckemon/flaskProject/diss.csv')


    # 각 열에 대해 레이블 인코더를 개별적으로 적용
    label_encoders = {}
    for column in df.columns:
        if df[column].dtype == 'object':  # 범주형 데이터만 변환
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le  # 각 열의 인코더 저장

    print("숫자형 데이터로 변환된 데이터프레임:")
    print(df)

    X = df.drop('선택한 포켓몬', axis=1)
    y = df['선택한 포켓몬']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SVM 모델 생성
    svm_model = SVC(kernel='linear', random_state=42)  # 선형 커널을 사용

    # 모델 훈련
    svm_model.fit(X_train, y_train)
    y_pred = svm_model.predict(X_test)

    # 정확도 계산
    accuracy = accuracy_score(y_test, y_pred)
    print(f'정확도: {accuracy:.2f}')

    # 분류 리포트 출력
    print("분류 리포트:")
    print(classification_report(y_test, y_pred))

    # 혼동 행렬 출력
    print("혼동 행렬:")
    print(confusion_matrix(y_test, y_pred))

    # 각 열을 다시 범주형 데이터로 복구
    for column in label_encoders:
        df[column] = label_encoders[column].inverse_transform(df[column])

    #포켓몬 대입
    pokemon_list = [pokemon.strip() for pokemon in input_pokemons.split(',')]
    new_data = {}
    for idx, p in enumerate(pokemon_list):
        key = f"{idx+1}위 라인업 추천 포켓몬"
        new_data[key] = p
    #
    # pokemon_1 = '따라큐' #@param {type:"raw"}
    # pokemon_2 = '몰드류' #@param {type:"raw"}
    # pokemon_3 = '아머까오' #@param {type:"raw"}
    # pokemon_4 = '잠만보' #@param {type:"raw"}
    # pokemon_5 = '에이스번' #@param {type:"raw"}
    # pokemon_6 = '미끄래곤' #@param {type:"raw"}
    # pokemon_7 = '파치래곤' #@param {type:"raw"}
    # pokemon_8 = '리자몽' #@param {type:"raw"}
    # pokemon_9 = '에이스번' #@param {type:"raw"}
    # pokemon_10 = '글레이시아' #@param {type:"raw"}
    # new_data = {'1위 라인업 추천 포켓몬' : pokemon_1, '2위 라인업 추천 포켓몬' : pokemon_2, '3위 라인업 추천 포켓몬' : pokemon_3, '4위 라인업 추천 포켓몬' : pokemon_4, '5위 라인업 추천 포켓몬' : pokemon_5, '6위 라인업 추천 포켓몬' : pokemon_6, '7위 라인업 추천 포켓몬' : pokemon_7,'8위 라인업 추천 포켓몬' : pokemon_8, '9위 라인업 추천 포켓몬' : pokemon_9, '10위 라인업 추천 포켓몬' : pokemon_10}
    new_data = pd.DataFrame([new_data])


    for column in new_data.columns:

        if column in label_encoders:  # 첫 번째 데이터에서 인코딩한 열이 있는지 확인

            new_data[column] = label_encoders[column].transform(new_data[column])  # 인코더를 사용하여 변환

    # new_data

    model = svm.SVC()
    model.fit(X_train, y_train)

    predictions = model.predict(new_data)

    predictions = pd.DataFrame(predictions, columns=['선택한 포켓몬'])

      # 각 열을 다시 범주형 데이터로 복구
    for column in predictions.columns:
        if column in label_encoders:
            predictions[column] = label_encoders[column].inverse_transform(predictions[column])


    recommandation = predictions['선택한 포켓몬'].values[0]

    print(f'당신의 라인업에 적당한 포켓몬은 {recommandation} 입니다.')
    return recommandation

# ai_recommend_pokemon('노말, 노말, 노말, 노말, 노말, 노말, 노말, 노말, 노말, 노말')
