from raw_text_preprocessing.table_creator import *

folder = ''

with open(folder + 'err.txt', 'r') as file:
    err_files = file.readlines()

for i in range(len(err_files) // 500 + 1):
    files = err_files[500*i:500*(i+1)]
    df_list = []
    for f in files:
        try:
            df_list.append(
                one_text_reader(folder + f[:-1])
            )
        except:
            with open(folder + 'err2.txt', 'a') as file:
                file.write(f + '\n')

    if len(df_list)!=0:
        pd.concat(df_list).to_csv(folder + 'data/res_table_2/table{}.csv'.format(i))




