from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('seller/',include('seller.urls')),
    path('cust/',include('customer.urls')),
]
