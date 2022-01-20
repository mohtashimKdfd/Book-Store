from .models import Customer
from seller.serializers import BookSerialize
from rest_framework import serializers


class CustomerSerialize(serializers.ModelSerializer):
    books_purchased = BookSerialize(read_only=True,many=True)
    class Meta:
        model = Customer
        fields = '__all__'