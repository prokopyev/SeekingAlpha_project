import pandas as pd
from bs4 import BeautifulSoup
import re
import os
from raw_text_preprocessing.table_creator import one_text_reader

wd = ''

# folders = ['data/inner/',
#            'data/outer/1-526/',
#            'data/outer/770-1046/',
#            'data/outer/1047-1241/',
#            'data/outer/1242-1894/']

# alltxts = []
# for f in folders:
#     alltxts += list(map(lambda x: wd+f+x, os.listdir(wd+f)))

alltxts = os.listdir('data/err_files')


def head_date(bstext):
    time_tags = bstext('time')
    head_time_list = [time_tags[0].get('datetime'),
                      time_tags[1].get('content'),
                      time_tags[1].text]
    return head_time_list


text_file = open(alltxts[0][5:].replace('*', '/'), "r")
lines = text_file.read()
text_file.close()
text = BeautifulSoup(lines, 'html.parser')




for f in alltxts:
    try:
        text_file = open(f[5:].replace('*', '/'), "r")
        lines = text_file.read()
        text_file.close()
        text = BeautifulSoup(lines, 'html.parser')
        print(head_date(text), head_comp(text))
    except:
        print(f)
        with open(wd+'debug_errors.txt', 'a') as file:
            file.write(f + '\n')







# for i in range(len(alltxts) // 500 + 1):
#     print(i)
#     files = alltxts[500 * i:500 * (i + 1)]
#     df_list = []
#     for f in files:
#         try:
#             df_list.append(
#                 one_text_reader(f)
#             )
#         except:
#             print(f)
#             with open(wd+'err.txt', 'a') as file:
#                 file.write(f + '\n')
#
#     pd.concat(df_list).to_csv(wd+'data/res_table_2/table{}.csv'.format(i))


