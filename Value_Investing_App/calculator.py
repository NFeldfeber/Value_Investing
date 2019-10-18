from Value_Investing_App.models import Stock, Financial_info


def calculate_intrinsic_value(stock):
    book_value_list = []
    for year_of_info in Financial_info.objects.filter(stock=stock):
        print("Total assets:", year_of_info.total_assets)
        print("Total liabilities:", year_of_info.total_liabilities)
        try:
            calculate_book_value(year_of_info)
            print(calculate_book_value(year_of_info))
        except TypeError:
            print("Cant calculate the book value for date", year_of_info.date)



def calculate_book_value(financial_info):
    return financial_info.total_assets - financial_info.total_liabilities

