from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404, render, redirect
from storeapp.forms import OrderForm, InterestForm, EditProfileForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views.generic import ListView
import datetime

# Create your views here.


class Index(ListView):
    model = Category, Product

    def get(self, request):
        cat_list = Category.objects.all().order_by('id')[:10]
        pro_list = Product.objects.all().order_by('-price')[:5]
        if 'last_login' not in request.session:
            msg = 'Your last login was more than one hour ago'
        else:
            msg = request.session['last_login']
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


def detail(request, cat_no):
    query = get_object_or_404(Category, id=cat_no)
    pro_list = Product.objects.filter(category__id=cat_no)
    return render(request, 'storeapp/detail.html', {'query': query, 'pro_list': pro_list})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'storeapp/products.html', {'prodlist': prodlist})


def place_order(request):
    if request.user.is_authenticated:
        msg = ''
        prodlist = Product.objects.all()
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                product = Product.objects.get(name=order.product.name)
                if order.num_units <= order.product.stock:
                    order.product.stock = order.product.stock - order.num_units
                    product.stock = order.product.stock
                    product.save()
                    order.client = Client.objects.get(first_name=request.user.first_name)
                    order.save()
                    msg = 'Your order has been placed successfully.'
                else:
                    msg = 'We do not have sufficient stock to fill your order. Try Again later..'
                    if order.product.stock <= 10:
                        product.refill()
                        product.save()
                return render(request, 'storeapp/order_response.html', {'msg': msg})

        else:
            form = OrderForm()
            return render(request, 'storeapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})
    else:
        request.session['place_order'] = 'True'
        return HttpResponseRedirect(reverse('storeapp:login'))


def productdetail(request, prod_id):
    prod = Product.objects.get(id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if request.POST['interested'] == '1':
                prod.interested = prod.interested + 1
                prod.save()
            return redirect('storeapp:index')
    else:
        form = InterestForm()
        return render(request, 'storeapp/productdetail.html', {'form': form, 'prod': prod})

def user_login(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('storeapp:index'))
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return render(request, 'storeapp/loginerror.html')
        else:
            return render(request, 'storeapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'storeapp/logout.html')


def myorders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(client__username=request.user)
        return render(request, 'storeapp/myorders.html', {'orders': orders, 'code': True})
    else:
        request.session['my_orders'] = '1'
        return HttpResponseRedirect(reverse('storeapp:login'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'storeapp/register.html', {'confirm': "Successfully Registered...!"})
    else:
        form = UserCreationForm()
        return render(request, 'storeapp/register.html', {'form': form})


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('storeapp:index')
        else:
            return render(request, 'storeapp/password.html', {'form': form, 'code': 1})
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'storeapp/password.html', {'form': form, 'code': 0})


def profile(request):
    prof = Client.objects.get(username=request.user)
    return render(request, 'storeapp/profile.html', {'prof': prof})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('storeapp:profile')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'storeapp/profile_edit.html', {'form': form})