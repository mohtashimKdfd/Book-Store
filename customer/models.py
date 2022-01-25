from django.db import models

from seller.models import Book

# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    books_purchased = models.ManyToManyField(Book)
    contact_number = models.IntegerField()
    otp = models.IntegerField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.username
