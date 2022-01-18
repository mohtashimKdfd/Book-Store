from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Book
from .serializers import BookSerialize

def home(request):
    return HttpResponse('<h1>Seller hun bhai</h1>')


def get(request):
    if request.method =="GET":
        books = Book.objects.all()
        serialized = BookSerialize(books,many=True)
        return JsonResponse(serialized.data,safe=False)