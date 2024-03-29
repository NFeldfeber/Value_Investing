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

from Value_Investing_App.models import Stock, Financial_info


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


def multiplying_factor():
    return 1000000


def format_financial_numbers_list(list):
    new_list = []
    for elem in list:
        new_list.append(elem*multiplying_factor())
    return new_list


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

    # Date of the income sheet
    dates_of_income_sheet = get_dates_of_tables(income_statement)
    print(dates_of_income_sheet)

    # Total Revenues
    texts_of_total_revenue = get_texts_by_row_title("Total Revenue", income_statement)
    total_revenue_list = format_list(texts_of_total_revenue, convert_money_to_int)
    total_revenue_list = format_financial_numbers_list(total_revenue_list)
    print(total_revenue_list)

    # Net Incomes
    text_of_net_incomes = get_texts_by_row_title("Net Income", income_statement)
    total_incomes_list = format_list(text_of_net_incomes, convert_money_to_int)
    total_incomes_list = format_financial_numbers_list(total_incomes_list)
    print(total_incomes_list)

    # Entering the Balance Sheet
    click_span_by_text("Balance Sheet", driver)
    time.sleep(2)
    driver.get(driver.current_url)
    time.sleep(5)
    balance_sheet = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(2)

    # Dates of the Balance Sheet info
    dates_of_balance_sheet = get_dates_of_tables(balance_sheet)
    print(dates_of_balance_sheet)
    time.sleep(5)
    # Total Assets
    texts_of_total_assets = get_texts_by_row_title("Total Assets", balance_sheet)
    total_assets_list = format_list(texts_of_total_assets, convert_money_to_int)
    total_assets_list = format_financial_numbers_list(total_assets_list)
    print(total_assets_list)
    time.sleep(2)
    # Total Liabilities
    texts_of_total_liabilities = get_texts_by_row_title("Total Liabilities", balance_sheet)
    total_liabilities_list = format_list(texts_of_total_liabilities, convert_money_to_int)
    total_liabilities_list = format_financial_numbers_list(total_liabilities_list)
    print(total_liabilities_list)
    time.sleep(2)
    # Long Term Debt
    texts_of_long_term_debt = get_texts_by_row_title("Long Term Debt", balance_sheet)
    total_long_term_debt_list = format_list(texts_of_long_term_debt, convert_money_to_int)
    total_long_term_debt_list = format_financial_numbers_list(total_long_term_debt_list)
    print(total_long_term_debt_list)
    time.sleep(2)

    # Entering the Statistics page
    click_span_by_text("Statistics", driver)
    time.sleep(2)
    driver.get(driver.current_url)
    time.sleep(5)
    statistics = BeautifulSoup(driver.page_source, 'html.parser')

    # Forward Annual Dividend Rate
    texts_of_dividend_rate = get_data_from_statistics_by_text("Forward Annual Dividend Rate", statistics)
    if texts_of_dividend_rate.upper() != "N/A":
        dividend_rate = float(texts_of_dividend_rate) / 100
    else:
        dividend_rate = 0
    print(dividend_rate)

    # Ammount of Shares
    texts_of_shares = get_data_from_statistics_by_text("Shares Outstanding", statistics)
    shares = shares_converter(texts_of_shares)
    print(shares)

    time.sleep(2)

    stock = Stock.objects.get(ticker=ticker)
    financial_info = []
    if len(dates_of_income_sheet) >= len(dates_of_balance_sheet):
        for index, date in enumerate(dates_of_income_sheet):
            is_ttm = False
            if date == datetime.now().date():
                is_ttm = True
            financial_info_year = Financial_info(stock=stock,
                                                 date=date,
                                                 is_ttm=is_ttm,
                                                 net_income=total_incomes_list[index],
                                                 total_revenue=total_revenue_list[index],
                                                 dividend_rate=dividend_rate,
                                                 ammount_of_shares=shares
                                                 )
            financial_info_year.save()
            financial_info.append(financial_info_year)
        for index, date in enumerate(dates_of_balance_sheet):
            for financial_info_elem in financial_info:
                if financial_info_elem.date == date:
                    print(date)
                    print(financial_info_elem.date)
                    print("Updating balance sheet info in already created financial info")
                    financial_info_stored = Financial_info.objects.get(stock=stock, date=date)
                    financial_info_stored.__setattr__('total_assets', total_assets_list[index])
                    financial_info_stored.__setattr__('total_liabilities', total_liabilities_list[index])
                    financial_info_stored.__setattr__('long_term_debt', total_long_term_debt_list[index])
                    financial_info_stored.save()
    else:
        for index, date in enumerate(dates_of_balance_sheet):
            is_ttm = False
            if date == datetime.now().date():
                is_ttm = True
            financial_info_year = Financial_info(stock=stock,
                                                 date=date,
                                                 is_ttm=is_ttm,
                                                 total_assets=total_assets_list[index],
                                                 total_liabilities=total_liabilities_list[index],
                                                 long_term_debt=total_long_term_debt_list[index],
                                                 dividend_rate=dividend_rate,
                                                 ammount_of_shares=shares
                                                 )
            financial_info_year.save()
            financial_info.append(financial_info_year)
        for index, date in enumerate(dates_of_balance_sheet):
            for financial_info_elem in financial_info:
                if financial_info_elem.date == date:
                    financial_info_stored = Financial_info.objects.get(stock=stock, date=date)
                    financial_info_stored.__setattr__('net_income', total_incomes_list[index])
                    financial_info_stored.__setattr__('total_revenue', total_revenue_list[index])
                    financial_info_stored.save()

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
            dates_of_info.append(datetime.now().date())
        else:
            splited_date = text_date.split('/')
            date = datetime(int(splited_date[2]), int(splited_date[0]), int(splited_date[1])).date()
            dates_of_info.append(date)
    return dates_of_info


def get_data_from_statistics_by_text(data_text, site):
    data = []
    row = site.find('span', text=data_text).parent.parent
    return row.find_all('td')[1].text


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


# todo TEST THIS FUNCTION
# Replace percentage with float (Ex: 10% = 0.1)
def convert_percentage_to_float(percentage_text):
    return float(percentage_text[:-1]) / 100


def shares_converter(shares_text):
    if shares_text[-1] == 'B':
        return float(shares_text[:-1]) * 1000000000000


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
