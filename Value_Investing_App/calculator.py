from Value_Investing_App.models import Stock, Financial_info
from Value_Investing_App.scraper import setup_driver
import time


def calculate_intrinsic_value(stock):
    calculate_value_via_web(stock)


def calculate_book_value_per_share(financial_info):
    return (financial_info.total_assets - financial_info.total_liabilities) / financial_info.ammount_of_shares


def calculate_value_via_web(stock):
    book_value_list = []
    financial_info_list = Financial_info.objects.filter(stock=stock, is_ttm=False).order_by("-date")

    for year_of_info in financial_info_list:
        print(year_of_info.date)
        try:
            print(calculate_book_value_per_share(year_of_info))
            book_value_list.append(calculate_book_value_per_share(year_of_info))
        except TypeError:
            print("Cant calculate the book value for date", year_of_info.date)

    # Dividend could be None
    dividend = financial_info_list.first().dividend_rate

    years_to_calculate = 10
    fed_percentage = 1.71

    base_url = "https://www.buffettsbooks.com/how-to-invest-in-stocks/intermediate-course/lesson-21/"
    driver = setup_driver(base_url)

    input_text = driver.find_elements_by_tag_name("input")
    input_text[0].send_keys(book_value_list[0].__str__())
    input_text[1].send_keys(book_value_list[-1].__str__())
    input_text[2].send_keys(len(book_value_list) - 1)

    input_text[3].click()

    input_text[5].send_keys(dividend.__str__())
    input_text[6].send_keys(book_value_list[0].__str__())
    input_text[7].send_keys(input_text[4].get_attribute("value"))
    input_text[8].send_keys(years_to_calculate)
    input_text[9].send_keys(fed_percentage.__str__())

    input_text[10].click()

    print(input_text[11].get_attribute("value"))
    time.sleep(5)
