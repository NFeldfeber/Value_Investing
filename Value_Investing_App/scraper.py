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
    driver = setup_driver(base_url)
    # Entering the Yahoo Finance site of the Business
    company_site_by_ticker(ticker, driver)

    # Entering the Financials of the business Page
    click_span_by_text("Financials", driver)
    time.sleep(2)

    # Retrieving the Income Statement data
    income_statement = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)
    print(income_statement.prettify())

    # Date of the income sheet
    dates_of_income_sheet = get_dates_of_tables(income_statement)
    print(dates_of_income_sheet)

    # Total Revenues
    texts_of_total_revenue = get_texts_by_row_title("Total Revenue", income_statement)
    total_revenue = format_list(texts_of_total_revenue, convert_money_to_int)
    print(total_revenue)

    # Net Incomes
    text_of_net_incomes = get_texts_by_row_title("Net Income", income_statement)
    total_incomes = format_list(text_of_net_incomes, convert_money_to_int)
    print(total_incomes)

    # Entering the Balance Sheet
    click_span_by_text("Balance Sheet", driver)
    balance_sheet = BeautifulSoup(driver.page_source, 'html.parser')

    # Dates of the Balance Sheet info
    dates_of_balance_sheet = get_dates_of_tables(balance_sheet)
    print(dates_of_balance_sheet)

    time.sleep(5)
    # driver.execute_script("window.history.go(-1)")

    driver.quit()
    # driver2.quit()


def click_span_by_text(text, driver):
    spans = driver.find_elements(By.TAG_NAME, "span")
    for span in spans:
        if span.text == text:
            span_to_click = span
    span_to_click.click()


def get_dates_of_tables(site):
    texts_of_dates = get_texts_by_row_title("Breakdown", site)
    dates_of_info = []
    # Formating the texts to datetime
    for text_date in texts_of_dates:
        if text_date.upper() == "TTM":
            dates_of_info.append(datetime.now())
        else:
            splited_date = text_date.split('/')
            date = datetime(int(splited_date[2]), int(splited_date[0]), int(splited_date[1]))
            dates_of_info.append(date)
    return dates_of_info


def format_list(original_list, converter):
    formatted_list = []
    for element in original_list:
        formatted_list.append(converter(element))
    return formatted_list


def convert_money_to_int(money_text):
    splitted_money = money_text.split(',')
    money = ""
    for figure in splitted_money:
        money += figure
    return int(money)


def get_texts_by_row_title(row_title, site):
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
    time.sleep(2)
    button.click()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
    finally:
        pass
