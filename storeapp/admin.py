from django.contrib import admin
from .models import Product, Category, Client, Order


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'get_interests')


# Register your models here.
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
admin.site.register(Product, ProductAdmin)
