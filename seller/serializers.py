
from pyexpat import model
from .models import Book, Seller
from rest_framework import serializers



class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['username']

class BookSerialize(serializers.ModelSerializer):
    sold_by = SellerSerializer(read_only=True)
    class Meta:
        model = Book
        fields = '__all__'