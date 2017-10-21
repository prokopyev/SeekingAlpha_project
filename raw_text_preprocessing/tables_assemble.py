import pandas as pd
import os

from raw_text_preprocessing.table_creator import one_text_reader



files = os.listdir('data/parsing')

df_list = []
for f in files:
    try:
        print(f)
        df_list.append(
            one_text_reader('data/parsing/' + f)
        )
    except:
        with open('err.txt', 'a') as file:
            file.write(f + '\n')















