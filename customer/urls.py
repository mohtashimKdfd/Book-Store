from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='Customer'),
    path('signup',views.signup,name='CustomerSignup'),
    path('login',views.login,name='CustomerLogin'),
    path('buy',views.buy,name='buy'),
    # path('profile',views.profile,name='customerProfile')
    path('otpverify',views.otpVerify,name='otpverify')
]
