from django.db import models


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    new = models.BooleanField(default=False)
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name