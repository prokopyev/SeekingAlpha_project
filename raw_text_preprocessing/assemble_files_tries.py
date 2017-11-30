import pandas as pd
from bs4 import BeautifulSoup
import re
import os
from raw_text_preprocessing.table_creator_v2 import one_text_reader

wd = ''

folders = ['data/inner/',
           'data/outer/1-526/',
           'data/outer/770-1046/',
           'data/outer/1047-1241/',
           'data/outer/1242-1894/']

alltxts = []
for f in folders:
    alltxts += list(map(lambda x: wd+f+x, os.listdir(wd+f)))


for i in range(len(alltxts) // 500 + 1):
    print(i)
    files = alltxts[500 * i:500 * (i + 1)]
    df_list = []
    for f in files:
        try:
            df_list.append(
                one_text_reader(f)
            )
        except:
            print(f)
            with open(wd+'err.txt', 'a') as file:
                file.write(f + '\n')

    pd.concat(df_list).to_csv(wd+'data/res_table_modified_func/table{}.csv'.format(i))





with open(wd + 'live_stream.txt', 'r') as file:
    lst = file.readlines()


