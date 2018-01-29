import pandas as pd
import os
import numpy as np


res_tabs = os.listdir('data/res_tables')

analutics_sa = []

for f in res_tabs:
    sares = pd.read_csv('data/res_tables/' + f)
    analutics_sa += list(pd.unique(sares['Analyst']))

analutics_sa = pd.unique(analutics_sa)

analutics_sa = analutics_sa[~pd.isnull(analutics_sa)].copy()





surnames = ['AGARWAL',
            'DENG',
            'MOCHORUK',
            'SHASTRI',
            'PERINCHERIL',
            'CHAOVAMU',
            'AFACAN',
            'SHEEHAN',
            'HOFFMANN',
            'KABANYANE',
            'EGEMEN',
            'BAKREN',
            'SLIPCHENKO',
            'GEOGHEGAN',
            'ANANDWALA',
            'SCHNECKENBURGER',
            'TOBIN',
            'CORNELL',
            'EATON',
            'DATTELS',
            'MICHEL',
            'BREMEN',
            'MOHSIN',
            'DMIRDJIAN',
            'FITZGERALD',
            'KRUEGER',
            'DUBOIS']






for s in surnames:

    print(s)

    for a in analutics_sa:
        if s.lower() in a.lower():
            print(a)






an = pd.read_stata('data/bran.dta')

an = an[an['baindi']=='A'].copy()


first = []

for i in pd.unique(an['baname']):
    if 'AGARWAL' in i:
        first.append(i)

second = []

for a in analutics_sa:
    if 'AGARWAL'.lower() in a.lower():
        second.append(a)

pd.DataFrame(first).to_csv('f.csv')
pd.DataFrame(second).to_csv('s.csv')
