import math
import pandas as pd
import ast
import numpy as np

pseeds=['기대', '긍정', '친환경', '투명', '책임', '상생', '소통', '저탄소', '달성', '친화', 
'공헌', '우수', '개선', '사회적', '동참', '가치', '적극', '녹색', '공정', '준법',
'지속가능', '신뢰', 'RE100', '윤리', '존중', '해결', '건강', '노력', '실천', 'CSR',
'공정', '수상', '안전', '그린', '창출']

nseeds=['위반', '불공정', '담합', '횡령', '갑질', '혐의', '분식회계', '퇴출', '불법', '의혹', 
'독과점', '산재', '논란', '괴롭힘', '오염', '피해', '조작', '미세먼지', '고발', '악용',
'불안', '구속', '물의', '박탈', '퇴출', '우려', '규탄', '비판', '반발', '빈축',
'악용', '불매', '부정', '아쉬움', '유리천장']



def so_pmi(w):
    pv=0
    for ps in pseeds:
        if ps in pmi:
            if w in pmi[ps]: 
                pv = pv + pmi[ps][w]

    nv=0
    for ns in nseeds:
        if ns in pmi:
            if w in pmi[ns]: 
                nv = nv + pmi[ns][w]

    return pv-nv


df = pd.read_csv('2018_2021_filtered.csv')
df['noun']  = df['noun'].map(lambda x : ast.literal_eval(x))

tokenized_data = []
for noun_list in df['noun']:
    tokenized_data.append(noun_list)
print(tokenized_data[:3])

corp=tokenized_data
print("Corp size=",len(corp))

dic={}
tot=0



dic2d={}
for d in corp:
    for w in d:
        tot+=1
        if w not in dic:
            dic[w]=1
        else:
            dic[w]+=1

    l=len(d)
    for i1 in range(0,l-1):
        for i2 in range(i1+1, l):
            w1=d[i1]
            w2=d[i2]
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


#x회 이상의 기사에 나온 단어만 쓰겠다
thr=100
print('Garbage collection.. Threshold=',thr)
print(len(dic),len(dic2d), '-->', end=' ')
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



fp1 = open('dic.csv', 'wt', encoding='utf-8')
fp1.write('key,freq\n')

for key in dic.keys():
    pr = dic[key]/tot
    #print(key, dic[key], tot, pr)
    #print('-'*50)
    fp1.write('%s,%f\n'%(key,dic[key]))

fp = open('dic2d.csv', 'wt', encoding='utf-8')
fp.write('key1,key2,freq,pmi\n')

pmi={}
for key1 in dic2d.keys():

    dsub=dic2d[key1]
    pmi[key1]={}
    for key2 in dsub.keys():
        pmiValue=math.log((dic2d[key1][key2]/tot)/((dic[key1]/tot)*(dic[key2]/tot))) #pmi 수식(값이 높을수록 관련성이 높다.)
        #print(key1, key2, dic2d[key1][key2], pmiValue)
        pmi[key1][key2]=pmiValue
        fp.write('%s,%s,%d,%f\n'%(key1,key2,dic2d[key1][key2], pmiValue))


fp2 = open('so_pmi.csv', 'wt', encoding='utf-8')
fp2.write('key,so_pmi\n')

for key in dic2d.keys():
    sp=so_pmi(key)
    #print(key, sp)
    fp2.write('%s,%f\n'%(key, sp) )
