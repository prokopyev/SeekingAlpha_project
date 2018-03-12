import pandas as pd
from bs4 import BeautifulSoup
import re


def check_string_in_list_strings(s, l):
    if len(s)>0:
        for el in l:
            if s in el:
                return True
    return False

# function retrieving text from given tag
def text_get(a):
    return a.text

# function dividing name of analyst or executive for person's name and company's name
def name_company_split(name):
    undef_list = ['Unidentified Company Representative',
                  'Unidentified Corporate Participant',
                  'Unidentified Analyst']
    undef_in = False
    for undef_id in undef_list:
        if undef_id in name:
            result_list = [undef_id, 'Unidentified Company']
            undef_in = True
            break
    if not undef_in:
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

def head_date(bstext):
    time_tags = bstext('time')
    head_time_list = [time_tags[0].get('datetime'),
                      time_tags[1].get('content'),
                      time_tags[1].text]
    return head_time_list

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

def head_comp(bstext):
    div_ahd = bstext('div', id="a-hd")[0]
    return div_ahd('h1')[0].text

def all_inf_date_comp(bstext, header):
    inf_list = []
    # comp_above, comp_head
    # date_above, date_mod, date_pub, date_pub_content
    # company part
    try:
        inf_list.append(comp_getter(header))
    except:
        inf_list.append('error')
    inf_list.append(head_comp(bstext))
    # date part
    try:
        inf_list.append(date_getter(header))
    except:
        inf_list.append('error')
    inf_list = inf_list + head_date(bstext)
    return inf_list


