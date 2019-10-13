from django.conf.urls import url
from django.urls import path
from Value_Investing_App import scraper
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('stock/<int:company_id>/', views.stock_detail, name='detail'),
    url(r'^stock/', views.stockList, name='stockList'),


]

