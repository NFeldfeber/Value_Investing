from random import randint
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

import re
import os


def stockTickerScraper():
    web = requests.get(
        "https://finance.yahoo.com/screener/unsaved/0994c99a-2c50-4557-9490-d3c21885c4b3")

    soup = BeautifulSoup(web.content, 'html.parser')
    table = soup.find("table")
    trs = table.select("tr")[1:]

    company_tickers = []
    company_name = []
    for tr in trs:
        for idx, td in enumerate(tr):
            if idx == 0:
                company_tickers.append(td.text)
            if idx == 1:
                company_name.append(td.text)
    print("Companies scraped: ", len(company_tickers))
    companies = zip(company_tickers, company_name)
    companies = list(companies)
    return companies


def stockInfoScraper(ticker):
    base_url = "https://finance.yahoo.com/"

    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    driver = webdriver.Chrome(r"C:\Users\Usuario\Desktop\Miscelaneous\chromedriver.exe")
    driver.get(base_url)
    driver.implicitly_wait(100)
    search_bar = driver.find_element_by_id("yfin-usr-qry")
    print(search_bar)
    search_bar.send_keys(ticker)
    time.sleep(5)
    # driver.execute_script("window.history.go(-1)")
    driver.quit()
