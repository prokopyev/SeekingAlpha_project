import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re



def text_get(a):
    return a.text


def name_company_split(name):
    r1 = name.split('–')
    r2 = name.split('-')
    result_list = 0
    if len(r1)==2:
        result_list = r1
    elif len(r2)==2:
        result_list = r2
    else:
        print('Error in splitting analytics name')
    return result_list


def date_getter(s):
    res = s.replace('Call End', '')
    res = res.replace('Call Start', '')
    first = r'[A-Z][a-z]+\,?\ +\d+\,? \d+\,?\;?\ +\d+?.?\d+.+'
    second = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +-\ +\d+?.?\d+.+'
    third = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +at\ +\d+?.?\d+.+'
    forth = r'[A-Z][a-z]+\,?\ +\d+\,? \d+'
    if len(re.findall(first, res))!=0:
        ret = re.findall(first, res)
    elif len(re.findall(second, res))!=0:
        ret = re.findall(second, res)
    elif len(re.findall(third, res))!=0:
        ret = re.findall(third, res)
    elif len(re.findall(forth, res)) != 0:
        ret = re.findall(forth, res)
    else:
        ret = res
    return ret[0].split('+')[0]


def one_text_reader(file_path):

    text_file = open(file_path, "r")
    lines = text_file.read()
    text_file.close()
    text = BeautifulSoup(lines, 'html.parser')

    text_data = text('p')

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

    header = '+'.join([(lambda x: x.text)(t) for t in text_data[:e_flag]])

    date = date_getter(header)
    # company_name = comp_getter(header)

    executives_name = []
    executives_pos = []
    for i in range(e_flag+1, a_flag):
        ex_text = text_data[i].text
        if len(ex_text)>0:
            executives_name.append(ex_text.split(' - ')[0])
            executives_pos.append(ex_text.split(' - ')[1])
    exec_dict = dict(zip([e.replace(' ', '') for e in executives_name], executives_pos))

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

                anal_name = name_company_split(one_q_sprint_data[0].text)[0]
                anal_comp = name_company_split(one_q_sprint_data[0].text)[1]
                exec_name = one_q_sprint_data[answers_ids[a_id]].text

                a = list(map(text_get, a))
                one_q_sprint.append(
                    [
                        company_name,                               # company
                        date,                                       # date
                        anal_name,                                  # analytics name
                        anal_comp,                                  # analytics company
                        ' '.join(q),                                # question
                        exec_name,                                  # exec name
                        exec_dict[exec_name.replace(' ', '')],      # exec company
                        ' '.join(a)                                 # answer
                    ]
                )
        result += one_q_sprint
    return pd.DataFrame(result, columns=['Company_name',
                                         'Date',
                                         'Analyst',
                                         'Analyst_bank',
                                         'Question',
                                         'Executive_Name',
                                         'Executive_position',
                                         'Answer'])



# r = one_text_reader("raw_text_preprocessing/1895_num_0.txt")


with open('err.txt', 'r') as file:
    t = file.read()

err_p = t.split('\n')

r = []
for p in err_p:

    text_file = open('data/parsing/' + p, "r")
    lines = text_file.read()
    text_file.close()
    text = BeautifulSoup(lines, 'html.parser')

    text_data = text('p')

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

    r.append(
        [(lambda x: x.text)(t) for t in text_data[:e_flag]]
    )

r_con = ['+'.join(x) for x in r]



def comp_getter(s):
    res = s.replace('Call End', '')
    res = res.replace('Call Start', '')
    if len(res)!=0:
        print(res)
        pat = re.findall(r'.+\([A-Z]+.+\)', res)[0]
    else:
        pat = res
    return pat


re.findall(r'.+\([A-Z]+.+\)', 'Owens-Illinois (NYSE:OI)+Q4 2012 Earnings Call+January 31, 2013  8:00 am ET')[0]


a = []
for i in range(len(r_con)):
    res = r_con[i]
    comp_getter(res)



r'.+\([A-Z]+:?[A-Z]+.?[A-Z]+\)'





# dates_list = []
# for res in r_con:
#     first = r'[A-Z][a-z]+\,?\ +\d+\,? \d+\,?\;?\ +\d+?.?\d+.+'
#     second = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +-\ +\d+?.?\d+.+'
#     third = r'[A-Z][a-z]+\,?\ +\d+\,?\ +\d+\ +at\ +\d+?.?\d+.+'
#     forth = r'[A-Z][a-z]+\,?\ +\d+\,? \d+'
#     if len(re.findall(first, res))!=0:
#         dates_list.append(
#             re.findall(first, res)
#         )
#     elif len(re.findall(second, res))!=0:
#         dates_list.append(
#             re.findall(second, res)
#         )
#     elif len(re.findall(third, res))!=0:
#         dates_list.append(
#             re.findall(third, res)
#         )
#     elif len(re.findall(forth, res)) != 0:
#         dates_list.append(
#             re.findall(forth, res)
#         )
#     else:
#         dates_list.append(res)






