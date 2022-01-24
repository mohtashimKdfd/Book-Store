from django.db import models

class Seller(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    contact_number = models.IntegerField()

    def __str__(self) -> str:
        return self.username

class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    new = models.BooleanField(default=False)
    price = models.IntegerField()
    sold_by =models.ManyToManyField(Seller) 

    def __str__(self) -> str:
        return self.name
