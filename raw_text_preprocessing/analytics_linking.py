import pandas as pd
import os
import numpy as np


res_tabs = os.listdir('data/res_tables')

analutics_sa = []

sares = pd.read_csv('data/res_tables/' + res_tabs[0])


for f in res_tabs:
    sares = pd.read_csv('data/res_tables/' + f)
    analutics_sa += list(pd.unique(sares['Analyst']))
    # analutics_sa += sum(list(map(lambda x: x.split(', '), pd.unique(sares['Analysts_list']))), [])

analutics_sa = pd.unique(analutics_sa)

analutics_sa = analutics_sa[~pd.isnull(analutics_sa)].copy()


# an = pd.read_stata('data/bran.dta')


list(pd.unique(sares['Analyst']))




recdet = pd.read_stata('data/recdet.dta')




sample = recdet.iloc[[3,100,1007,4321, 70000, 5, 6, 20,  1678,62465,45114,9000,60000,43351], :].copy()


surdict = {}

for s in pd.unique(recdet['cname'])[:500]:#list(map(lambda x: x.split(' ')[0], sample['analyst'].tolist())):

    print(s)

