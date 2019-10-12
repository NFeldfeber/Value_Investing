from django.db import models


# Create your models here.


class Stock(models.Model):
    company_name = models.CharField(max_length=300)
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.company_name
