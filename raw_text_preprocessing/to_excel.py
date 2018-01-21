import pandas as pd
import os

tables = os.listdir('data/res_table_modified_func')

for t in tables:
    temp_t = pd.read_csv('data/res_table_modified_func/' + t)
    temp_t.to_excel(t[:-4] + '.xlsx')



