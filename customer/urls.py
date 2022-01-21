from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='Customer'),
    path('signup',views.signup,name='CustomeSignup'),
    path('login',views.login,name='CustomerLogin'),
    path('buy',views.buy,name='buy')
]
