import MeCab
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
import pymysql
import sqlalchemy





data = pd.read_csv('esg_dataset_2021.csv')
data['word_list'] = np.nan
data = data.astype('object')

print(data.dtypes)

from collections import Counter
    
#count = Counter(data.loc[0][3])
print(data.loc[0][3])    


for i in range(len(data)):    
    count = Counter(data.loc[i][3])
    tag_count = []
    tags = []
    
    
    for n, c in count.most_common(100):
    
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2 and len(tags) <= 49:
            tag_count.append(dics)
            tags.append(dics['tag'])
            
            data.at[i,'word_list'] = tags['count']
    
    for tag in tag_count:
    
        print(" {:<14}".format(tag['tag']), end='\t')
    
        print("{}".format(tag['count']))
        print("\n---------------------------------")
        print("     명사 총  {}개".format(len(tags)))
        print("---------------------------------\n\n")
        
    
