from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader

from Value_Investing_App.models import Stock
from Value_Investing_App.scraper import stockTickerScraper
from . import scraper


def index(request):
    template = loader.get_template('Value_Investing_App/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def stockList(request):
    scraping = request.POST.get('Scrape')
    print(Stock.objects.all().count())
    Stock.objects.all().delete()
    print(Stock.objects.all().count())
    if scraping:
        companies = stockTickerScraper()
        for company in companies:
            stock = Stock(company_name=company[1], ticker=company[0])
            stock.save()

    stock_list = Stock.objects.all()
    template = loader.get_template('Value_Investing_App/stock_list.html')
    context = {
        'stock_list': stock_list,
    }
    print("asd")
    return HttpResponse(template.render(context, request))


def scrapeTickers(request):
    stockTickerScraper()
    stockList(request)
