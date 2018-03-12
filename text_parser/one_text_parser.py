import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np

from text_parser.elements_parser_funcs import *



###################################################################

def check_file_fullness(text_data, log_folder):
    for p in range(len(text_data)):
        if 'question-and-answer session not available' in text_data[p].text.lower():
            with open(log_folder + 'log.txt', 'a') as file:
                file.write("no_q-a_session ------ " + file_path + "\n")
            return True
        if 'no q&a session for this event' in text_data[p].text.lower():
            with open(log_folder + 'log.txt', 'a') as file:
                file.write("no_q-a_session ------ " + file_path + "\n")
            return True
    if len(text_data) <= 7:
        with open(log_folder + 'log.txt', 'a') as file:
            file.write("short_text-livestream ------ " + file_path + "\n")
        return True
    return False



def get_head_info(text_data, bstext):
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
    comp_date_inf = all_inf_date_comp(bstext, header)

    executives_name = []
    executives_pos = []
    for i in range(e_flag+1, a_flag):
        ex_text = text_data[i].text
        if len(ex_text)>0:
            executives_name.append(name_company_split(ex_text)[0])
            executives_pos.append(name_company_split(ex_text)[1])
    executives_name = list(map(lambda x: x.strip(), executives_name))
    executives_pos = list(map(lambda x: x.strip(), executives_pos))
    exec_dict = dict(
        zip(
            executives_name,
            executives_pos
        )
    )

    analysts = []
    for i in range(a_flag+1, stop_flag):
        a_text = text_data[i].text
        if len(a_text)>0:
            cur_analyst = name_company_split(a_text)
            cur_analyst = list(map(lambda x: x.strip(), cur_analyst))
            analysts.append(cur_analyst)
    analysts_dict = dict(analysts)

    return comp_date_inf, exec_dict, analysts_dict



def qa_start_find(text_data):
    QA_begin = 0
    for p in range(len(text_data)):
        if text_data[p].get('id') == "question-answer-session":
            QA_begin = p
            break
    return QA_begin



def get_oper_chunks(text_data, qa_start):
    oper_flags = []
    for p in range(qa_start, len(text_data)):
        if '<strong>Operator' in str(text_data[p]):
            oper_flags.append(
                p
            )
    oper_chunks =  []
    for f in range(len(oper_flags) - 1):
        oper_chunks.append(
            text_data[oper_flags[f]:oper_flags[f + 1]]
        )
    return oper_chunks



def get_qa_chunks(oper_chunk, analysts_dict):
    q_blocks = []
    respective_analysts = []
    for p in range(len(oper_chunk)):
        # if p_data[p].text in analysts:
        if check_string_in_list_strings(oper_chunk[p].text.replace(' ', ''),
                                        list(map(lambda x: x.replace(' ', ''), analysts_dict.keys()))):
            q_blocks.append(p)
            respective_analysts.append(oper_chunk[p].text)
    qa_chunks = []
    for i in range(len(q_blocks) - 1):
        qa_chunks.append(
            oper_chunk[q_blocks[i]:q_blocks[i + 1]]
        )
    return qa_chunks, respective_analysts



def get_qa_pairs(qa_chunk, exec_dict):

    qa_pairs = []

    q = []
    for j in range(1, len(qa_chunk)):
        if qa_chunk[j].text.replace(' ', '') in [e.replace(' ', '') for e in exec_dict.keys()]:
            break
        q.append(qa_chunk[j].text)

    respective_executives = []
    answers_ids = []
    for j in range(1, len(qa_chunk)):
        if qa_chunk[j].text.replace(' ', '') in [e.replace(' ', '') for e in exec_dict.keys()]:
            answers_ids.append(j)
            respective_executives.append(qa_chunk[j].text)
    answers_ids.append(len(qa_chunk))

    for a_id in range(len(answers_ids) - 1):
        a = qa_chunk[answers_ids[a_id] + 1:answers_ids[a_id + 1]]
        qa_pairs.append([
            ' '.join(q), ' '.join(list(map(text_get, a)))
        ])
    return qa_pairs, respective_executives


##### second part #####

def check_n_qas(text):
    n_qas = len(text.find_all("span", attrs={"class":"question"})) + \
            len(text.find_all("span", attrs={"class":"answer"}))
    if n_qas>0:
        return True
    else:
        return False



def get_marked_qas(text_data, text):
    answers = pd.unique(list(
            map(
                str,
                text.find_all("span", attrs={"class":"answer"})
            )))
    questions = pd.unique(list(
            map(
                str,
                text.find_all("span", attrs={"class":"question"})
            )))
    qa_indexes = []
    qa_str_index = []
    for p in range(len(text_data)):
        for a in answers:
            if a in str(text_data[p]):
                qa_indexes.append(p)
                qa_str_index.append('a')
        for q in questions:
            if q in str(text_data[p]):
                qa_indexes.append(p)
                qa_str_index.append('q')

    qa_chunks_inds = []
    for i in range(len(qa_indexes)-1):
        qa_chunks_inds.append(
            [qa_indexes[i], qa_indexes[i+1]]
        )

    last_ind = qa_indexes[-1]+1

    if text_data[last_ind].text!=0:
        qa_chunks_inds.append(
            [qa_indexes[-1], last_ind+1]
        )
    else:
        qa_chunks_inds.append(
            [qa_indexes[-1], last_ind+2]
        )

    table_from_classes = []
    for i in range(len(qa_chunks_inds)-1):
        name = text_data[qa_chunks_inds[i][0]].text
        sentences_list = text_data[qa_chunks_inds[i][0]+1:qa_chunks_inds[i][1]]
        sentences_list = list(map(lambda x: x.text, sentences_list))
        sentences = " ".join(sentences_list)
        if qa_str_index[i]=='a':
            sentence_type = 'answer'
        elif qa_str_index[i]=='q':
            sentence_type = 'question'

        table_from_classes.append([
            name,
            sentences,
            sentence_type
        ])

    return pd.DataFrame(table_from_classes, columns=['Name', 'Speech', 'QA_indicator'])



def process_second_df(df, comp_date_inf, exec_dict, analysts_dict):
    df['Order'] = [i+1 for i in range(len(df))]
    df = pd.concat([
        df,
        pd.DataFrame([comp_date_inf] * len(df),
                     columns=['Company_name',
                              'Company_name_head',
                              'Date',
                              'Date_modified',
                              'Date_published',
                              'Date_published_dup'])], axis=1)
    df = pd.concat([df,
                   pd.DataFrame([[str(analysts_dict), str(exec_dict)]] * len(df),
                                columns=['Analysts_list','Executives_list'])],
                   axis=1)
    return df


##### main f #####

def one_text_reader(file_path, log_folder=''):

    result = []

    result_df_columns = ['Company_name',
                         'Company_name_head',
                         'Date',
                         'Date_modified',
                         'Date_published',
                         'Date_published_dup',
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
                         'File_path']

    text_file = open(file_path, "r")
    lines = text_file.read()
    text_file.close()
    text = BeautifulSoup(lines, 'html.parser')
    text_data = text('p')

    skip_iter_flag = check_file_fullness(text_data, log_folder)

    if skip_iter_flag:
        return pd.DataFrame(columns=result_df_columns)
    else:
        comp_date_inf, exec_dict, analysts_dict = get_head_info(text_data, text)


        if check_n_qas(text):
            df_marked = get_marked_qas(text_data, text)
            df_marked = process_second_df(df_marked, comp_date_inf, exec_dict, analysts_dict)
            df_marked['File_path'] = file_path
        else:
            df_marked = pd.DataFrame(columns=['Name', 'Speech', 'QA_indicator', 'Order',
                                              'Company_name', 'Company_name_head',
                                              'Date', 'Date_modified', 'Date_published',
                                              'Date_published_dup',
                                              'Analysts_list','Executives_list', 'File_path'])

        qa_start = qa_start_find(text_data)

        oper_chunks = get_oper_chunks(text_data, qa_start)

        analytics_order = 0
        for o in range(len(oper_chunks)):

            oper_chunk = oper_chunks[o]
            qa_chunks, respective_analysts = get_qa_chunks(oper_chunk, analysts_dict)

            analytics_order += 1
            question_order = 0
            for qa in range(len(qa_chunks)):

                qa_chunk = qa_chunks[qa]
                qa_pairs, respective_executives = get_qa_pairs(qa_chunk, exec_dict)

                question_order += 1
                answer_oredr = 0
                for i_pair in range(len(qa_pairs)):

                    qa_pair = qa_pairs[i_pair]

                    answer_oredr += 1

                    analytics_name = respective_analysts[qa]
                    analytics_comp = analysts_dict[analytics_name]
                    executive_name = respective_executives[i_pair]
                    executive_comp = exec_dict[executive_name]
                    q = qa_pair[0]
                    a = qa_pair[1]

                    result.append([
                        comp_date_inf[0],   # company
                        comp_date_inf[1],   # company_header
                        comp_date_inf[2],   # date
                        comp_date_inf[3],   # date mod
                        comp_date_inf[4],   # date pub
                        comp_date_inf[5],   # date pub content
                        analytics_name,     # analytics name
                        analytics_comp,     # analytics company
                        q,                  # question
                        executive_name,     # exec name
                        executive_comp,     # exec company
                        a,                  # answer
                        analytics_order,    # analytics_order
                        question_order,     # analytics_q_order
                        answer_oredr,       # exec_a_order
                        str(analysts_dict), # dict of analysts
                        str(exec_dict),     # dcit of executives
                        file_path           # path_to_file
                    ])

    result_df = pd.DataFrame(result, columns=result_df_columns)

    return result_df, df_marked







# wd = ''
# file_path = wd + 'data/outer/1242-1894/1759_num_9.txt'
#
# df1, df2 = one_text_reader(file_path)







