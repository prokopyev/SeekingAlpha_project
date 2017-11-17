import pandas as pd
from bs4 import BeautifulSoup
import re
from raw_text_preprocessing.table_creator import *

with open('err.txt', 'r') as file:
    err_files = file.readlines()

file_path = err_files[10][:-1]


file_path = 'data/inner/3000_num_10.txt'


### func start ###

text_file = open(file_path, "r")
result = []

lines = text_file.read()
text_file.close()
text = BeautifulSoup(lines, 'html.parser')

text_data = text('p')

for p in range(len(text_data)):
    if 'Unidentified Company Representative' in text_data[p].text:
        print('Unidentified Company Representative included')
        break

e_flag = 0
a_flag = 0
stop_flag = 0
for p in range(len(text_data)):
    if 'Executives' in text_data[p].text:
        e_flag = p
    elif 'Executive' in text_data[p].text:
        e_flag = p
    if 'Analysts' in text_data[p].text:
        a_flag = p
    elif 'Analyst' in text_data[p].text:
        a_flag = p
    if 'Operator' in text_data[p].text:
        stop_flag = p
        break

print(e_flag, a_flag, stop_flag)

header = '+'.join([(lambda x: x.text)(t) for t in text_data[:e_flag]])

date = date_getter(header)
company_name = comp_getter(header)

executives_name = []
executives_pos = []
for i in range(e_flag + 1, a_flag):
    ex_text = text_data[i].text
    if len(ex_text) > 0:
        executives_name.append(name_company_split(ex_text)[0])  # ex_text.split(' - ')[0])
        executives_pos.append(name_company_split(ex_text)[1])
exec_dict = dict(zip([e.replace(' ', '') for e in executives_name], executives_pos))

analysts = []
for i in range(a_flag + 1, stop_flag):
    a_text = text_data[i].text
    if len(a_text) > 0:
        analysts.append(a_text)

QA_begin = 0
for p in range(len(text_data)):
    if text_data[p].get('id') == "question-answer-session":
        QA_begin = p
        break

oper_flags = []
for p in range(QA_begin, len(text_data)):
    if '<strong>Operator' in str(text_data[p]):
        oper_flags.append(
            p
        )

analytics_order = 0
for f in range(len(oper_flags) - 1):

f = 0
p_data = text_data[oper_flags[f]:oper_flags[f + 1]]
q_blocks = []
for p in range(len(p_data)):
    if p_data[p].text in analysts:
        q_blocks.append(p)

analytics_order += 1

one_q_sprint = []
sprint_order = 0
for i in range(len(q_blocks) - 1):

one_q_sprint_data = p_data[q_blocks[i]:q_blocks[i + 1]]

q = []
for j in range(1, len(one_q_sprint_data)):
    if one_q_sprint_data[j].text.replace(' ', '') in [e.replace(' ', '') for e in executives_name]:
        break
    q.append(one_q_sprint_data[j].text)

answers_ids = []
for j in range(1, len(one_q_sprint_data)):
    if one_q_sprint_data[j].text.replace(' ', '') in [e.replace(' ', '') for e in executives_name]:
        answers_ids.append(j)
answers_ids.append(len(one_q_sprint_data))

sprint_order += 1

answer_oredr = 0
for a_id in range(len(answers_ids) - 1):
    a = one_q_sprint_data[answers_ids[a_id] + 1:answers_ids[a_id + 1]]

    anal_name = name_company_split(one_q_sprint_data[0].text)[0]
    anal_comp = name_company_split(one_q_sprint_data[0].text)[1]
    exec_name = one_q_sprint_data[answers_ids[a_id]].text
    exec_list = list(
        map(lambda x: x[0] + '-' + x[1],
            list(zip(executives_name, executives_pos))
            )
    )

    a = list(map(text_get, a))

    answer_oredr += 1
    one_q_sprint.append(
        [
            company_name,  # company
            date,  # date
            anal_name,  # analytics name
            anal_comp,  # analytics company
            ' '.join(q),  # question
            exec_name,  # exec name
            exec_dict[exec_name.replace(' ', '')],  # exec company
            ' '.join(a),  # answer
            analytics_order,  # analytics_order
            sprint_order,  # analytics_q_order
            answer_oredr,  # exec_a_order
            analysts,  # list of analysts
            exec_list,  # list of executives
            file_path  # file
        ]
    )
result += one_q_sprint

pd.DataFrame(result, columns=['Company_name',
                          'Date',
                          'Analyst',
                          'Analyst_bank',
                          'Question',
                          'Executive_Name',
                          'Executive_position',
                          'Answer',
                          'Analytics_order',
                          'Analytics_question_order',
                          'Exec_answer_order',
                          'Analysts_list',
                          'Executives_list',
                          'File_path'])











