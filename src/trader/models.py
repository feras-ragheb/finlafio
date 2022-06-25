from tkinter import CURRENT
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Trader(models.Model):
    GENDER=[('M',_('Male')),
         ('F',_('Female'))]
    COUNTRY=[('USA',_('United State Of America')),('UK',_('United King Dom'))]     
    first_name=models.CharField(max_length=20)
    last_name = models.CharField(max_length=35)
    nickname = models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER, max_length=2)
    country=models.CharField(choices=COUNTRY,max_length=5)
    user = models.ForeignKey(User,related_name="trader_user_fk" ,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)


    def __str__(self):
        return self.first_name + self.last_name

class TradeFavorit(models.Model):
    SOURCE = [(1,_('Stocks')),(2,_('News Websit1e')),(3,_('Influencer'))]
    trader = models.ForeignKey(Trader, related_name='favorit_trade_fk',on_delete=models.CASCADE)
    source_type=models.CharField(max_length=3,choices=SOURCE)
    source_values=models.JSONField()


    def __str__(self):
        return str(trader__first_name)