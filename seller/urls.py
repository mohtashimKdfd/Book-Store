from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='SellerHome'),
    path('get',views.get,name='Get')
]
