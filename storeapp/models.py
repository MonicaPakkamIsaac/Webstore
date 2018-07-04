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


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]

    company = models.CharField(max_length=50, null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)
    image = models.ImageField(null=True, blank=True, upload_to='display_picture')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def get_interests(self):
        return ",".join([str(p) for p in self.interested_in.all()])


class Order(models.Model):
    ORDER_CHOICES = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=1)
    order_status = models.IntegerField(choices=ORDER_CHOICES, default='1')
    status_date = models.DateField(default=timezone.now)

    def total_cost(self):
        return '%d' % (self.product.price * self.num_units)

    def __str__(self):
        return '%s - %s/%s' % (self.client.username, self.product, self.status_date)