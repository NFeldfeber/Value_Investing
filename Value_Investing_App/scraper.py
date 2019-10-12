from time import sleep

import requests
from bs4 import BeautifulSoup


def stockScraper():
    web = requests.get(
        "https://finance.yahoo.com/screener/predefined/most_actives")

    # print(web.status_code)
    soup = BeautifulSoup(web.content, 'html.parser')
    trs = soup.find_all("tr")[1:]

    company_names = []

    for tr in trs:
        for idx, td in enumerate(tr):
            if idx == 1:
                company_names.append(td.text)

    return company_names
