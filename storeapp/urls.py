from django.urls import path
from django.conf.urls import url
from storeapp import views
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_done, password_reset_confirm

app_name = 'storeapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:cat_no>', views.detail, name='detail'),
    path(r'place_order', views.place_order, name='place_order'),
    path(r'products', views.products, name='products'),
    path(r'products/<int:prod_id>', views.productdetail, name='productdetail'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myorders', views.myorders, name='myorders'),
    ]