import self as self
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.template import loader
from django.views.generic import DetailView

from Value_Investing_App.models import Stock
from Value_Investing_App.scraper import stockTickerScraper, stockInfoScraper
from . import scraper
from django.views import generic


def index(request):
    template = loader.get_template('Value_Investing_App/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def stockList(request):
    scraping = request.POST.get('Scrape')

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
    return HttpResponse(template.render(context, request))


def scrapeTickers(request):
    stockTickerScraper()
    stockList(request)


def stock_detail(request, company_id):
    template_name = 'Value_Investing_App/detail.html'
    stock = Stock.objects.filter(id=company_id).first()
    print(stock)
    stockInfoScraper(stock.ticker)

    context = {
        'stock': stock,
    }
    return render(request, template_name, context)
