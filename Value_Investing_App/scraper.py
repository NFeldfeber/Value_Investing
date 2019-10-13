from random import randint
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    driver = setup_driver(base_url)
    company_site_by_ticker(ticker, driver)

    link = driver.find_elements(By.TAG_NAME,"span")
    print(link)
    for elem in link:
        if(elem.text=="Financials"):
            elem.click()

    time.sleep(5)

    # driver.execute_script("window.history.go(-1)")

    driver.quit()


def setup_driver(url):
    driver = webdriver.Chrome(r"C:\Users\Usuario\Desktop\Miscelaneous\chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(100)
    return driver


def company_site_by_ticker(ticker, driver):
    search_bar = driver.find_element_by_id("yfin-usr-qry")
    button = driver.find_element_by_tag_name("button")
    search_bar.send_keys(ticker)
    time.sleep(5)
    button.click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    finally:
        time.sleep(2)
