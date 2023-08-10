import pandas as pd
import matplotlib.pyplot as plt
import pymysql
import datetime
import math
import os


def so_pmi(w):
    pv=0
    for ps in pseeds:
        if ps in pmi:
            if w in pmi[ps]: pv+=pmi[ps][w]

    nv=0
    for ns in nseeds:
        if ns in pmi:
            if w in pmi[ns]: nv+=pmi[ns][w]

    return pv-nv



maxrow=76420
connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='1234', db='esg')

cursor = connect.cursor()

stopWords=['뉴시스', '연합', '뉴스', '서울', '기자']

pseeds=['기대', '긍정', '친환경', '투명', '책임', '상생', '소통', '저탄소', '달성', '친화', 
'공헌', '우수', '개선', '사회적', '동참', '가치', '적극', '녹색', '공정', '준법',
'지속가능', '신뢰', 'RE100', '윤리', '존중', '해결', '건강', '노력', '실천', 'CSR',
'공정', '수상', '안전', '그린', '창출']

nseeds=['위반', '불공정', '담합', '횡령', '갑질', '혐의', '분식회계', '퇴출', '불법', '의혹', 
'독과점', '산재', '논란', '괴롭힘', '오염', '피해', '조작', '미세먼지', '고발', '악용',
'불안', '구속', '물의', '박탈', '퇴출', '우려', '규탄', '비판', '반발', '빈축',
'악용', '불매', '부정', '아쉬움', '유리천장']

print(len(pseeds), len(nseeds))
dic={}
dic2d={}
pmiValue={}
tot=0

#단어, 단어별 빈도
if os.path.isfile('dic.csv'):
    fp=open('dic.csv', 'r', encoding='utf-8')
    while True:
        l=fp.readline()
        if not l:break
        l=l.replace('\n','')
        ls=l.split(',')
        if ls[0]=='key': continue
        dic[ls[0]]=int(ls[1])
        dic2d[ls[0]]={}
        pmiValue[ls[0]]={}
    fp.close()


#두 단어 사이의 빈도
if os.path.isfile('dic2d.csv'):
    fp=open('dic2d.csv', 'r', encoding='utf-8')
    while True:
        l=fp.readline()
        if not l:break
        l=l.replace('\n','')
        ls=l.split(',')
        if ls[0]=='key1': continue
        w1=ls[0]
        w2=ls[1]
        freq=int(ls[2])
        pmi=float(ls[3])
        #print(w1,w2)
        dic2d[w1][w2]=freq
        pmiValue[w1][w2]=pmi

start=1
if os.path.isfile('upto.csv'):
    fp=open('upto.csv','r')
    start=int(fp.readline())+1
    fp.close()


flog=open('log.txt', 'wt')

for id in range(start,maxrow+1):
    query="SELECT noun FROM esg_crawl_6year_copy WHERE id=%d"%(id)
    if id%100==0: 
        print(query, len(dic))
        flog.write(query+' , %d\n'%len(dic))
        flog.flush()

    cursor.execute(query)
    result = cursor.fetchall()

    for record in result:
        wordsStr = record[0]
        #print(wordsStr)
        wordsStr=wordsStr.replace(',저작,연합,뉴스,단전,재재,배포,금지', '')
        words=wordsStr.split(',')
        words2=[]

        #단어별빈도수
        for w in words:
            if len(w)==0: continue
            if w in stopWords: continue

            tot+=1
            if w not in dic:
                dic[w]=1
            else:
                dic[w]+=1

            words2.append(w)
            #print('w=',w)

        #전체 단어(words2)
        l=len(words2)
        for i1 in range(0,l):
            for i2 in range(0, l):
                if i1==i2: break
                w1=words2[i1]
                w2=words2[i2]
                #print('w1=',w1)
                #print('w2=',w2)
                if w1 not in dic2d:
                    dic2d[w1]={}
                if w2 not in dic2d[w1]:
                    dic2d[w1][w2]=1
                else:
                    dic2d[w1][w2]+=1

                if w2 not in dic2d:
                    dic2d[w2]={}
                if w1 not in dic2d[w2]:
                    dic2d[w2][w1]=1
                else:
                    dic2d[w2][w1]+=1


    if id==maxrow:    
        #x회 이상의 기사에 나온 단어만 쓰겠다
        thr=int(id/1000)
        print('Garbage collection.. Threshold=',thr)
        print(len(dic),len(dic2d), '-->', end=' ')
        flog.write('Garbage collection: %d, %d --> '%(len(dic),len(dic2d)))
        flog.flush()
        #안쓰는 단어 제거한 2차원 배열
        if thr>1:
            newdic={}
            for k in dic:
                if dic[k]>=thr: newdic[k]=dic[k]
            
            dic=newdic
            nd2={}
            for k1 in dic.keys():
                nd2[k1]={}
            for k1 in dic.keys():
                for k2 in dic.keys():
                    n1=0
                    if k1 in dic2d:
                        if k2 in dic2d[k1]:
                            n1=dic2d[k1][k2]
                    if n1>0: nd2[k1][k2]=n1
                    
                    n2=0
                    if k2 in dic2d:
                        if k1 in dic2d[k2]:
                            n2=dic2d[k2][k1]
                    if n2>0: nd2[k2][k1]=n2
            dic2d=nd2
        print(len(dic),len(dic2d))
        flog.write('%d, %d\n'%(len(dic),len(dic2d)))
        flog.flush()

        fp = open('upto.csv', 'wt', encoding='utf-8')
        fp.write('%d\n'%id)
        fp.close()

        fp = open('dic.csv', 'wt', encoding='utf-8')
        fp.write('key,freq\n')
        for key in dic.keys():
            fp.write('%s,%d\n'%(key,dic[key]))
        fp.close()


        fp = open('dic2d.csv', 'wt', encoding='utf-8')
        fp.write('key1,key2,freq,pmi\n')
        pmi={}
        for key1 in dic2d.keys():
            dsub=dic2d[key1]
            pmi[key1]={}
            #딕셔너리라 느림;;
            for key2 in dsub.keys():
                pmiValue=math.log((dic2d[key1][key2]/tot)/((dic[key1]/tot)*(dic[key2]/tot)))
                #print(key1, key2, dic2d[key1][key2], pmiValue)
                fp.write('%s,%s,%d,%f\n'%(key1,key2,dic2d[key1][key2], pmiValue) )
                pmi[key1][key2]=pmiValue
        fp.close()

        fp2 = open('so_pmi.csv', 'wt', encoding='utf-8')
        fp2.write('key,so_pmi\n')
        #key 단어
        for key in dic2d.keys():
            sp=so_pmi(key)
            #print(key, sp)
            fp2.write('%s,%f\n'%(key, sp) )

        fp2.close()

        connect.close()#####
        exit()#####

connect.close()


##############
