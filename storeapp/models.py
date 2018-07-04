from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=100, null=False, blank=False, default=' ')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100, validators={})
    available = models.BooleanField(default=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def refill(self, num=0):
        if num:
            self.stock = self.stock + num
            self.save()
        else:
            self.stock = self.stock + 100
            self.save()

    def __str__(self):
        return self.name