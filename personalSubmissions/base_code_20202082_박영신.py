import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score



def parsing(path):#파싱을 진행하는 함수
    with open(path,'r',encoding='utf-8') as f:#파일을 읽어드리고 ['로그','로그',...] 이런식으로 로그를 구조화
        train=[]
        para=""
        while True:
            l = f.readline() #한줄씩 읽어 옵니다
    
            if not l:
                break #파일을 전부 읽으면 읽기를 중단합니다.

            if l != "\n":   #첫줄에는 URI가 있기 때문에 포함합니다.
                para +=l

            while l != "\n":    #필요없는 줄은 넘어갑니다.
                l = f.readline()

            if para!='':
                if para[:4]=='POST' or para[:3] == 'PUT':   #POST와 PUT에 대해서는 body를 포함합니다.
                    para+=f.readline()
                train.append(para)
                para=""
                
    return train

def dataset(path,mod='train'): #데이터셋을 생성합니다. 파싱한 데이터와 라벨을 생성합니다 
    x = parsing(f'{path}norm_{mod}.txt') # mod에 따라 train을 가져올지 test 데이터를 가져올지 결정됩니다.
    y = [0]*len(x) # 정상 라벨 0 을 정상 데이터 개수 만큼 생성
    x += parsing(f'{path}anomal_{mod}.txt')
    y += [1]*(len(x)-len(y)) # 비정상 라벨 1을 비정상 데이터 개수 만큼 생성
    return x, y

def vectorize(train_x,test_x): #문장을 벡터로 만듭니다 해당 코드에서는 기본적인 tf idf를 사용하고 있습니다.
    tf = TfidfVectorizer(analyzer="char", ngram_range = (3,3)) #trigram을 사용합니다.
    tf = tf.fit(train_x)
    train_vec = tf.transform(train_x)
    test_vec = tf.transform(test_x)
    return train_vec,test_vec

def train(train_vec,train_y): #랜덤 포레스트로 훈련 시킵니다. 모델을 바꾸고 싶다면 이 함수를 변경해야 합니다.
    rf = RandomForestClassifier()
    rf.fit(train_vec,train_y)
    return rf

def test(test_y,test_vec,rf): #입력 받은 테스트와 모델로 테스트를 실시합니다
    pred = rf.predict(test_vec)
    print(accuracy_score(test_y,pred))
    print(f1_score(test_y,pred))
    return pred


def run():
############### 실행 코드 #######################
################################################
    train_x, train_y = dataset('./','train')
    test_x, test_y =  dataset('./','test')

    train_vec, test_vec = vectorize(train_x, test_x)
    rf = train(train_vec, train_y)
    pred = test(test_y,test_vec, rf)

########################################################
    tf = TfidfVectorizer()
    tf = tf.fit(train_x)

    # print(len(tf.vocabulary_)) # 고유한 단어가 대략 8만개가 나옵니다

    # print(tf.transform(train_x)[0]) #로그 하나당 약 8만차원이 나옵니다
                                # 필요없는 문장 때문에 단어의 개수가 많이 진것일  수도 있으니 데이터를 분석하여 필요한 부분만 사용하는것이 좋습니다


if __name__=="__main__":
    run()   
