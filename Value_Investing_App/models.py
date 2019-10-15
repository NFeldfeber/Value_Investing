from django.core.exceptions import ObjectDoesNotExist
from django.db import models


# Create your models here.


class Stock(models.Model):
    company_name = models.CharField(max_length=300)
    ticker = models.CharField(max_length=10)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        try:
            Stock.objects.get(company_name=self.company_name, ticker=self.ticker)
        except ObjectDoesNotExist:
            super().save(*args, **kwargs)  # Call the "real" save() method.
        else:
            print(self.company_name, " is already saved")


class Financial_info(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField('Information Date')
    is_ttm = models.BooleanField('Is TTM Info', default=False)
    total_revenue = models.FloatField('Total Revenue', null=True, blank=True)
    net_income = models.FloatField('Net Income', null=True, blank=True)
    total_assets = models.FloatField('Total Assets', null=True, blank=True)
    total_liabilities = models.FloatField('Total Liabilities', null=True, blank=True)
    long_term_debt = models.FloatField('Long Term Debt', null=True, blank=True)
    dividend_rate = models.FloatField('Dividend Rate', default=0)

    def __str__(self):
        return self.stock.ticker + " Financials"
