from random import randint
import time

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


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import re
import os


def stockScraper2():
    base_url = "https://finance.yahoo.com/screener/unsaved/7d145dd6-4dc6-40d6-a519-48f4b4e86746"

    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    company_ticker = []
    trs = soup.find_all("tr")[1:]
    for tr in trs:
        for idx, td in enumerate(tr):
            if idx == 0:
                company_ticker.append(td.text)

    print(company_ticker)

    driver = webdriver.Chrome(r"C:\Users\Usuario\Desktop\Miscelaneous\chromedriver.exe")
    driver.get(base_url)
    driver.implicitly_wait(5)

    random_num = randint(0, 24)
    for ticker in company_ticker[:25]:
        print("Searching for ticker ", ticker)
        ticker_link = driver.find_element_by_link_text(ticker)
        ticker_link.click()
        time.sleep(3)
        driver.execute_script("window.history.go(-1)")