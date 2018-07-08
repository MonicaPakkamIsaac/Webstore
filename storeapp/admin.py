from django.contrib import admin
from .models import Product, Category, Client, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')


# Register your models here.
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
