from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
import datetime

# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    pro_list = Product.objects.all().order_by('-price')[:5]
    return render(request, 'storeapp/index.html', {'cat_list': cat_list, 'pro_list': pro_list, 'msg': msg})


def about(request):
    heading2 = 'This is an Online store APP'
    if 'about_visits' in request.COOKIES:
        about_visits = int(request.COOKIES.get('about_visits')) + 1
        response = render(request, 'storeapp/about.html',
                          {'content': heading2, 'visits': about_visits})
        response.set_cookie('about_visits', str(about_visits), max_age=300)
    else:
        response = render(request, 'storeapp/about.html',
                          {'content': heading2, 'visits': 1})
        response.set_cookie('about_visits', '1')
    return response