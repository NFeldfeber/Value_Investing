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
    companies = zip(company_tickers,company_name)
    companies = list(companies)
    print(companies)
    print(companies[0])
    print(companies[0][0])
    return companies


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
    driver.implicitly_wait(100)

    for ticker in company_ticker[0:25]:
        print("Searching for ticker ", ticker)
        ticker_link = driver.find_element_by_link_text(ticker)
        try:
            ticker_link.click()
        except Exception.StaleElementReferenceException as e:
            print(e)

        time.sleep(5)
        driver.execute_script("window.history.go(-1)")
    driver.quit()
