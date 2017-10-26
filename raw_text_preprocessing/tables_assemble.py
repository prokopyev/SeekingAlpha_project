import pandas as pd
import os

from raw_text_preprocessing.table_creator import one_text_reader

folder = '../'

files = os.listdir(folder + 'data/parsing')

df_list = []
for f in files:
    try:
        df_list.append(
            one_text_reader(folder + 'data/parsing/' + f)
        )
    except:
        print(f)
        with open(folder + 'err.txt', 'a') as file:
            file.write(f + '\n')

pd.concat(df_list).to_csv(folder + 'table.csv')

### save errors files

with open(folder + 'err.txt', 'r') as file:
    err_files = file.readlines()


from shutil import copyfile


for f in err_files[:-1]:
    f = f.replace('\n', '')
    copyfile('data/parsing/' + f, 'data/' + f)

