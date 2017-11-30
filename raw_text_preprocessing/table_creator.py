import pandas as pd
from bs4 import BeautifulSoup
import re



# function retrieving text from given tag
def text_get(a):
    return a.text

# function dividing name of analyst or executive for person's name and company's name
def name_company_split(name):
    utf_name = name.encode('utf-8')
    result_list = [name, 'No_company_found']
    if b'\xe2\x80\x93' in utf_name:
        result_list = utf_name.split(b'\xe2\x80\x93')
        result_list = [result_list[0].decode(), result_list[1].decode()]
    elif '-' in name:
        result_list = name.split('-')
    result_list = [result_list[0], ' - '.join(result_list[1:])]
    return result_list

# function gets date from given str
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

# def comp_getter(s):
#     res = s.replace('Call End', '')
#     res = res.replace('Call Start', '')
#     pat = re.findall(r'.+\([A-Z]+.+\)', res)[0]
#     if '+' in pat:
#         parts = pat.split('+')
#         if :
#             pass
#         else:
#             for p in parts:
#                 search_c = re.search(r'\(.+[A-Z]+\)', p)
#                 if search_c is not None:
#                     search_c = search_c.group()
#                 else:
#                     search_c = ""
#                 if len(search_c)!=0:
#                     pat = p
#     return pat


def comp_getter(s):
    res = s.replace('Call End', '')
    res = res.replace('Call Start', '')
    try:
        pat = re.findall(r'.+\([A-Z]+.+\)', res)[0]
        if '+' in pat:
            parts = pat.split('+')
            if 'Inc' in parts[0]:
                pat = re.findall(r'.+Inc{?}*', parts[0])[0]
            else:
                for p in parts:
                    search_c = re.search(r'\(.+[A-Z]+\)', p)
                    if search_c is not None:
                        search_c = search_c.group()
                    else:
                        search_c = ""
                    if len(search_c)!=0:
                        pat = p
    except:
        if '+' in res:
            parts = res.split('+')
            if 'Inc' in parts[0]:
                pat = re.findall(r'.+Inc{?}*', parts[0])[0]
            else:
                for p in parts:
                    search_c = re.search(r'\(.+[A-Z]+\)', p)
                    if search_c is not None:
                        search_c = search_c.group()
                    else:
                        search_c = ""
                    if len(search_c)!=0:
                        pat = p
    return pat


# mail function - get table from given text (text as hole page with QA session)
def one_text_reader(file_path):
    folder = ''
    result = []

    text_file = open(file_path, "r")
    lines = text_file.read()
    text_file.close()
    text = BeautifulSoup(lines, 'html.parser')
    text_data = text('p')

    for p in range(len(text_data)):
        if 'question-and-answer session not available' in text_data[p].text:
            with open(folder + 'err_qa_not_available.txt', 'a') as file:
                file.write(file_path + '\n')
            break
        if 'No Q&A session for this event' in text_data[p].text:
            with open(folder + 'err_qa_not_available.txt', 'a') as file:
                file.write(file_path + '\n')
            break

    e_flag = 0
    a_flag = 0
    stop_flag = 0
    for p in range(len(text_data)):
        if len(text_data[p].contents) != 0:
            if 'Executives' in text_data[p].text:
                e_flag = p
            elif '<strong>Executive' in str(text_data[p].contents[0]):
                e_flag = p
            if 'Analysts' in text_data[p].text:
                a_flag = p
            elif '<strong>Analyst' in str(text_data[p].contents[0]):
                a_flag = p
            if '<strong>Operator' in str(text_data[p].contents[0]):
                stop_flag = p
                break

    header = '+'.join([(lambda x: x.text)(t) for t in text_data[:e_flag]])

    date = date_getter(header)
    company_name = comp_getter(header)

    executives_name = []
    executives_pos = []
    for i in range(e_flag+1, a_flag):
        ex_text = text_data[i].text
        if len(ex_text)>0:
            executives_name.append(name_company_split(ex_text)[0]) #ex_text.split(' - ')[0])
            executives_pos.append(name_company_split(ex_text)[1])
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
            if 'question-and-answer session not available' in text_data[p].text:
                with open(folder + 'err_qa_not_available.txt', 'a') as file:
                    file.write(file_path + '\n')
            break

    oper_flags = []
    for p in range(QA_begin, len(text_data)):
        if '<strong>Operator' in str(text_data[p]):
            oper_flags.append(
                p
            )

    analytics_order = 0
    for f in range(len(oper_flags) - 1):
        p_data = text_data[oper_flags[f]:oper_flags[f + 1]]
        q_blocks = []
        for p in range(len(p_data)):
            # if p_data[p].text in analysts:
            if p_data[p].text.replace(' ', '') in list(
                        map(lambda x: x.replace(' ', ''), analysts)
            ):
                q_blocks.append(p)

        analytics_order+=1

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

            sprint_order+=1

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

                answer_oredr+=1
                one_q_sprint.append(
                    [
                        company_name,                               # company
                        date,                                       # date
                        anal_name,                                  # analytics name
                        anal_comp,                                  # analytics company
                        ' '.join(q),                                # question
                        exec_name,                                  # exec name
                        exec_dict[exec_name.replace(' ', '')],      # exec company
                        ' '.join(a),                                # answer
                        analytics_order,                            # analytics_order
                        sprint_order,                               # analytics_q_order
                        answer_oredr,                               # exec_a_order
                        str(analysts)[1: -1],                                   # list of analysts
                        str(exec_list)[1:-1],                                  # list of executives
                        file_path
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
                                         'Answer',
                                         'Analytics_order',
                                         'Analytics_question_order',
                                         'Exec_answer_order',
                                         'Analysts_list',
                                         'Executives_list',
                                         'File_path'])



# r = one_text_reader("raw_text_preprocessing/1895_num_0.txt")

