import MeCab
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
import pymysql
import sqlalchemy

#데이터프레임 수정
data0 = pd.read_csv('url_dataset_2021.csv')
data = pd.read_csv('text_url_2021.csv')
data['noun'] = np.nan
data['press'] = data0['press']
data['date'] = data0['date']
data['word_list'] = np.nan
data = data.astype('object')

#??
def preproc(words):
    w2 = []
    for i, t in enumerate(words):
        w, p = t
        w=w.replace('"','\\quot')
        w=w.replace('ᆫ', 'ㄴ')
        w=w.replace('ᆯ', 'ㄹ')
        w=w.replace('ᆷ', 'ㅁ')
        w=w.replace('ᆸ', 'ㅂ')

        p=p.replace('NNBC', 'NNB') # 세종품사태그로 변환
        p=p.replace('SY', 'SO')
        p=p.replace('SC', 'SP')
        w2.append((w, p))
    return w2

#형태소 추출 코드
def posTag(text):
    tagger = MeCab.Tagger()
    s = tagger.parse(text)
    l = s.split('\n')
    pos=[]
    for item in l:
        if item=='EOS':
            break
        i2 = item.split('\t')
        i3 = i2[1].split(',')
        #print(i3)

        if '+' in i3[0]:
            t1=i3[5]
            t2=i3[6]
            w1=i3[7].split('/')[0]
            w2=(i3[7].split('+')[1]).split('/')[0]

            i = (w1, t1)
            pos.append(i)
            i = (w2, t2)
            pos.append(i)
        else:
            i = (i2[0], i3[0])
            pos.append(i)

            
    return pos

#??
def phraseTag(sent, subLevel=False, debug=False):
    tagged = posTag(sent)
    tagged = preproc(tagged)
    #print(tagged)
    posList=[]
    for token in tagged:
        posList.append(token[0]+'/'+token[1])

    #print(posList)
    return posList



for i in range(len(data)):
    data.loc[i]['content'] = data.loc[i][2].replace('flash 오류를 우회하기 위한 함수 추가', '')
    data.loc[i]['content'] = data.loc[i][2].replace('function _flash_removeCallback() {}', '')


#불용어
stop_words = ['사진제공', '무단', '전재', '배포', '특종']

#본문 내용중 NNG, NNP만 추출하여 Noun 컬럼에 입력
for i in range(len(data)):
    #print(data.loc[i][0])
    #print(i)    
    nouns = []
    a = posTag(data['content'][i]) # 형태소 분석 코드
    #print(a)
    a_nouns = [n for n, tag in a if tag in ["NNG","NNP"]] #명사만 추출
    #print(a_nouns)
    #불용어 제거
    for w in a_nouns:
        if w not in stop_words:
            nouns.append(w)

    data.at[i,'noun'] = nouns

print(data.loc[52][3])
print(data.loc[53][3])

#data.to_csv('esg_dataset_2021.csv', encoding = 'utf-8-sig', index=False)

#print(data.loc[5]['noun'])
