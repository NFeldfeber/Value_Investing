from django.conf.urls import url

from Value_Investing_App import scraper
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^stocks/', views.stockList, name='stockList'),


]