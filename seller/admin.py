from django.contrib import admin
from .models import Book , Seller
# Register your models here.

admin.site.register(Seller)

@admin.register(Book)
class bookAdmin(admin.ModelAdmin):
    list_display = ['name','author','price']
