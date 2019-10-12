from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from django.template import loader

from Value_Investing_App.models import Stock
from . import scraper

def index(request):
    template = loader.get_template('Value_Investing_App/index.html')
    context = {

    }
    return HttpResponse(template.render(context,request))


def stockList(request):
    stock_list = scraper.stockScraper()
    # stock_list = Stock.objects.all()
    template = loader.get_template('Value_Investing_App/stock_list.html')
    context = {
        'stock_list': stock_list,
    }
    return HttpResponse(template.render(context, request))


