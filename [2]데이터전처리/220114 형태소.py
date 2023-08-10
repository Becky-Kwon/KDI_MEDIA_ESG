import MeCab
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
import pymysql
import sqlalchemy



#데이터프레임 수정
data = pd.read_csv('보고서 텍스트 데이터.csv')
data['noun'] = np.nan   
data = data.astype('object')


#db 입력
conn = pymysql.connect(host='127.0.0.1', user='root', password='1234',db='esg_db', charset='utf8mb4')
cursor = conn.cursor()

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
        p=p.replace('SC', 'SP')5
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


#본문 전처리
# =============================================================================
# for i in range(len(data)):
#     data.loc[i]['content'] = data.loc[i]['content'].replace('flash 오류를 우회하기 위한 함수 추가', '')
#     data.loc[i]['content'] = data.loc[i]['content'].replace('function _flash_removeCallback() {}', '')
# =============================================================================


#불용어사전
stop_words = ['사진제공', '무단', '전재', '배포', '특종', '기자', 
              '증권부장', '무단전재', '재배포', '뉴스', '기사', '구독신청', '머니', '투데이', '리얼타임', '부장', '뉴시스', '운세', '실검', 
              '데일리' '뉘', '우', '스', '그동안', '생방송', 'com', 'kr', 'newsis', 'yesphoto', 'www', '클릭', '신문', 'co', 'seoul', 'mk'
              #언론사
              '머니투데이', '매일경제', '뉴시스', '아이뉴스24', '더팩트', '디지털데일리', '국민일보', '한경비즈니스', '일간스포츠', '파이낸셜뉴스', 
              '한국경제', '서울신문', '이데일리', '전자신문', '세계일보', '연합뉴스', 'KBS', 'ZDNet Korea', '헤럴드경제', '머니S', '매경이코노미', 
              '서울경제', 'MBN', '아시아경제', '블로터', '조선일보', '뉴스1', 'SBS Biz', '데일리안', '경향신문', '중앙일보', '조세일보', '조선비즈', '스포츠동아', 
              '한국경제TV', '노컷뉴스', '디지털타임스', 'YTN', '스포츠조선', '코리아헤럴드', '문화일보', '중앙SUNDAY', '코리아중앙데일리', '스포츠서울', 'MBC', '동아일보', 
              '한국일보', '부산일보', 'SBS', '오마이뉴스', '연합뉴스TV', '한겨레', '스타뉴스', '프레시안', '주간동아', 
              '신동아', '주간조선', '이코노미스트', '인벤', '여성신문', 'TV조선', '동아사이언스', '비즈니스워치', '스포츠경향', '매일신문', 
              'OSEN', '스포츠월드', 'JTBC GOLF', 'MK스포츠', '인터풋볼', '스포탈코리아', '코메디닷컴', '미디어오늘', '시사저널', '주간경향']



#본문 내용중 NNG, NNP만 추출하여 Noun 컬럼에 입력
for i in range(len(data)):
# =============================================================================
#     conn = pymysql.connect(host='127.0.0.1', user='root', password='1234',db='esg_db', charset='utf8mb4')
#     cursor = conn.cursor()
# =============================================================================
    #print(data.loc[i][0])
    #print(i)    
    nouns = []
    a = posTag(data['내용'][i]) # 형태소 분석 코드
    #print(a)
    a_nouns = [n for n, tag in a if tag in ["SL","NNG","NNP"]] #명사만 추출
    
    #불용어 제거
    for w in a_nouns:
        if w not in stop_words:
            nouns.append(w)
    
    data.at[i,'noun'] = nouns #데이터프레임에 입력  


# DB 입력
# # 
#     noun_db = ' '.join(s for s in nouns)          #리스트 문자열로 변경
#     
#     sql = """ 
#           INSERT INTO esg_url_crawl(noun) VALUES(%s)
#     """
#     cursor.execute(sql,noun_db)
#     conn.commit()
# # 
# 
# =============================================================================

#CSV 입력
#data.to_csv('esg_dataset_2021.csv', encoding = 'utf-8-sig', index=False)


#언론사 추출 
# =============================================================================
# press = []
# for i in range(len(data)):
# 
#     press.append(data.loc[i]['press'])
#     
# result = [] 
# for w in press:
#     if w not in result:
#         result.append(w)
# 
# print(result)
# 
# 
# =============================================================================

#확인용(지우기)
# =============================================================================
# c = posTag(data.iloc[0]['content'])
# c_nouns = [n for n, tag in c if tag in ["SL","NNG","NNP"]] #명사만 추출
# c_nounss = []
# 
# 
# for w in c_nouns:
#     if w not in stop_words:
#         c_nounss.append(w)
# 
# print(c_nounss)
# =============================================================================
