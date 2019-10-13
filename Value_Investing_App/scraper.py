from random import randint
import time
from datetime import datetime

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

    # driver = setup_driver(base_url)

    # Entering the Yahoo Finance site of the Business
    # company_site_by_ticker(ticker, driver)

    # Entering the Financials of the business Page
    # link = driver.find_elements(By.TAG_NAME,"span")
    # for elem in link:
    #     if(elem.text=="Financials"):
    #         span_to_click = elem
    # span_to_click.click()

    # Retrieving the Income Statement data

    driver2 = webdriver.Chrome(r"C:\Users\Usuario\Desktop\Miscelaneous\chromedriver.exe")
    driver2.get("https://finance.yahoo.com/quote/AAPL/financials?p=AAPL")
    income_statement = BeautifulSoup(driver2.page_source, 'html.parser')

    #Date of the information
    text_of_dates = get_text_by_row_title("Breakdown", income_statement)
    dates_of_info = []
    #Formating the texts to datetime
    for text_date in text_of_dates:
        if text_date.upper() == "TTM":
            dates_of_info.append(datetime.now())
        else:
            splited_date = text_date.split('/')
            date = datetime(int(splited_date[2]), int(splited_date[0]), int(splited_date[1]))
            dates_of_info.append(date)
    print(dates_of_info)

    #Total revenues
    total_revenue = []
    text_of_total_revenue = get_text_by_row_title("Total Revenue", income_statement)
    for text_data in text_of_total_revenue:
        splitted_revenue = text_data.split(',')
        total_revenue.append(int(splitted_revenue[0] + splitted_revenue[1] + splitted_revenue[2]))
    print(total_revenue)
    time.sleep(10)
    # driver.execute_script("window.history.go(-1)")

    # driver.quit()
    driver2.quit()


def get_text_by_row_title(row_title,site):
    data = []
    row = site.find('span', text=row_title).parent.parent.parent
    for spans in row.find_all('span')[1:]:
        data.append(spans.text)
    return data

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
