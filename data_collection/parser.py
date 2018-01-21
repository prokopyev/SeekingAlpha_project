import numpy as np

import requests
from bs4 import BeautifulSoup
import time

from user_agent import generate_user_agent

url_art = 'https://seekingalpha.com/earnings/earnings-call-transcripts/'  # + number
url_site = 'https://seekingalpha.com/'

folder = '../'

h = generate_user_agent() #next(headers)
page = requests.get(url_art + str(3330), headers={'User-Agent': h})
page_bs = BeautifulSoup(page.text, "lxml")
links = page_bs.findAll('ul', id='analysis-list-container')[0]
links = links.findAll('h3')
arts = []
for a in links:
    arts.append(a.findAll('a')[0]['href'])

h = generate_user_agent() #next(headers)
page_art = requests.get(url_site + arts[5], headers={'User-Agent': h})

# headers = header_change()

for i in range(3329, 4565):

    print(i)

    try:
        h = generate_user_agent() #next(headers)
        page = requests.get(url_art + str(i), headers={'User-Agent': h})
        page_bs = BeautifulSoup(page.text, "lxml")
        links = page_bs.findAll('ul', id='analysis-list-container')[0]
        links = links.findAll('h3')
        arts = []
        for a in links:
            arts.append(a.findAll('a')[0]['href'])
        for x in range(0, len(arts)):
            h = generate_user_agent() #next(headers)
            page_art = requests.get(url_site + arts[x], headers={'User-Agent': h})
            print(page_art.text)
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












