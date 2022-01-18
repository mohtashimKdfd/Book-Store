from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

def home(request):
    return HttpResponse('<h1>Customer hun bhai</h1>')