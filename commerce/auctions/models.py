from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comment(models.Model):
    user = models.CharField(max_length=20)
    comment = models.TextField(max_length=100)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    listing_id = models.IntegerField()

class Lis(models.Model):  
    name = models.CharField(max_length=64)
    owner = models.CharField(max_length=32)
    description = models.TextField(max_length=800)
    price = models.IntegerField()
    category = models.CharField(max_length=32)
    img = models.CharField(max_length=150, blank=True, default=None)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    
class Bids(models.Model):
    bid = models.IntegerField()
    user = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    listing_id = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()

class ClosedLis(models.Model):
    winprice = models.IntegerField()
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64) 
    name = models.CharField(max_length=64)
    listing_id = models.IntegerField()


class AllLis(models.Model):  
    name = models.CharField(max_length=64)
    owner = models.CharField(max_length=32)
    description = models.TextField(max_length=800)
    price = models.IntegerField()
    category = models.CharField(max_length=32)
    img = models.CharField(max_length=150, blank=True, default=None)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)