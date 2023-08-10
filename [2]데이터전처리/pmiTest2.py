import math
import pandas as pd

nseeds=['부정', '우려']
pseeds=['기대', '시급']

n1=['우려', '반발', '부정']
n2=['우려', '곤란', '반발']
n3=['반발', '부정', '곤란']


p1=['기대', '필요', '적극']
p2=['시급', '필요', '적극']
p3=['기대', '필요', '시급']


corp=[n1,n2,n3,p1,p2,p3]

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

for key in dic.keys():
    pr = dic[key]/tot
    print(key, dic[key], tot, pr)
    print('-'*50)


pmi={}
for key1 in dic2d.keys():
    dsub=dic2d[key1]
    pmi[key1]={}
    for key2 in dsub.keys():
        pmiValue=math.log((dic2d[key1][key2]/tot)/((dic[key1]/tot)*(dic[key2]/tot))) #pmi 수식(값이 높을수록 관련성이 높다.)
        print(key1, key2, dic2d[key1][key2], pmiValue)
        pmi[key1][key2]=pmiValue
