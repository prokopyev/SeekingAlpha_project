import numpy as np

import requests
from bs4 import BeautifulSoup
import time

from user_agent import generate_user_agent

def header_change():
    header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/' +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             '.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    header2 = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/' +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             '.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
    header3 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/' +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             '.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    header4 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/' +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             '.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    header5 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/' +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             str(np.random.randint(1, high=9)) +
                             '.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    headers = [header1, header2, header3, header4, header5]
    while True:
        for h in headers:
            yield h

url_art = 'https://seekingalpha.com/earnings/earnings-call-transcripts/'  # + number
url_site = 'https://seekingalpha.com/'

folder = '../'

# headers = header_change()

for i in range(3329, 4565):

    print(i)

    try:
        h = generate_user_agent() #next(headers)
        page = requests.get(url_art + str(i), headers={'User-Agent': h})
        page_bs = BeautifulSoup(page.text, "lxml")
        print(page_bs)
        links = page_bs.findAll('ul', id='analysis-list-container')[0]
        links = links.findAll('h3')
        arts = []
        for a in links:
            arts.append(a.findAll('a')[0]['href'])
        for x in range(0, len(arts)):
            h = generate_user_agent() #next(headers)
            page_art = requests.get(url_site + arts[x], headers={'User-Agent': h})
            try:
                if page_art.status_code == 200:
                    page_bs_art = BeautifulSoup(page_art.text, "lxml")
                    text = page_bs_art.findAll('article')[0]

                    with open(folder + "data/parsing/" + str(i) + '_num_' + str(x) + '.txt', "w") as f:
                        f.write(str(text))

                    print(str(i) + '_num_' + str(x) + '.txt')

                else:
                    h = generate_user_agent() #next(headers)
                    time.sleep(15)
                    page_art = requests.get(url_site + arts[x], headers={'User-Agent': h})
                    page_bs_art = BeautifulSoup(page_art.text, "lxml")
                    text = page_bs_art.findAll('article')[0]

                    with open(folder + "data/parsing/" + str(i) + '_num_' + str(x) + '.txt', "w") as f:
                        f.write(str(text))

                    print(str(i) + '_num_' + str(x) + '.txt')

            except:
                h = generate_user_agent() #next(headers)
                time.sleep(50)
                with open(folder + "data/errors.txt", "a") as f:
                    f.write(url_site + arts[x])

    except:
        time.sleep(50)
        with open(folder + "data/big_errors.txt", "a") as f:
            f.write(url_site + str(i))