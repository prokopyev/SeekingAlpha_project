import pandas as pd
import numpy as np
from bs4 import BeautifulSoup



text_file = open("raw_text_preprocessing/1895_num_0.txt", "r")
lines = text_file.read()
text_file.close()
text = BeautifulSoup(lines, 'html.parser')

text_data = text('p')

company_name = text.p.contents[0] + text.p.a.contents[0] + ")"
quarter = text_data[1].contents[0][:7]
date = text_data[2].contents[0]

e_flag = 0
a_flag = 0
stop_flag = 0
for p in range(len(text_data)):
    if 'Executives' in text_data[p].text:
        e_flag = p
    if 'Analysts' in text_data[p].text:
        a_flag = p
    if 'Operator' in text_data[p].text:
        stop_flag = p
        break

executives_name = []
executives_pos = []
for i in range(e_flag+1, a_flag):
    ex_text = text_data[i].text
    if len(ex_text)>0:
        executives_name.append(ex_text.split(' - ')[0])
        executives_pos.append(ex_text.split(' - ')[1])

analysts = []
for i in range(a_flag+1, stop_flag):
    a_text = text_data[i].text
    if len(a_text)>0:
        analysts.append(a_text)

QA_begin = 0
for p in range(len(text_data)):
    if text_data[p].get('id')=="question-answer-session":
        QA_begin = p
        break

oper_flags = []
for p in range(QA_begin, len(text_data)):
    if '<strong>Operator' in str(text_data[p]):
        oper_flags.append(
            p
        )

result = []
for f in range(len(oper_flags) - 1):
    p_data = text_data[oper_flags[f]:oper_flags[f + 1]]
    q_blocks = []
    for p in range(len(p_data)):
        if p_data[p].text in analysts:
            q_blocks.append(p)

    one_q_sprint = []
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

        for a_id in range(len(answers_ids) - 1):
            a = one_q_sprint_data[answers_ids[a_id] + 1:answers_ids[a_id + 1]]


            def text_get(a):
                return a.text


            a = list(map(text_get, a))
            one_q_sprint.append(
                [
                    one_q_sprint_data[0].text,  # analytics name
                    ' '.join(q),  # question
                    one_q_sprint_data[answers_ids[a_id]].text,  # exec name
                    ' '.join(a)  # answer
                ]
            )
    result += one_q_sprint

pd.DataFrame(result).to_csv('test.csv')




























