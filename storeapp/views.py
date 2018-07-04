from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
import datetime

# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    pro_list = Product.objects.all().order_by('-price')[:5]
    return render(request, 'storeapp/index.html', {'cat_list': cat_list, 'pro_list': pro_list, 'msg': msg})
