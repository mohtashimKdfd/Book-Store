from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer
from .serializers import CustomerSerialize
from rest_framework.decorators import api_view


def home(request):
    customers = Customer.objects.all()
    print(customers)
    serializedCustomer = CustomerSerialize(customers,many=True)
    return JsonResponse(serializedCustomer.data,safe=False)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        username = request_body['username']
        password = request_body['password']
        number = request_body['number']
        if Customer.objects.filter(username=username).exists():
            return JsonResponse('User Already Exists || Try login',status=400,safe=False)
        
        newCustomer = Customer(username=username,password=make_password(password),contact_number=number)
        newCustomer.save()

        return JsonResponse('Customer Account created',status=201,safe=False)

@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':
        # print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body["username"]
        password = body['password']
        if Customer.objects.filter(username=username).exists():
            targetCustomer = Customer.objects.get(username=username)
            if check_password(password,targetCustomer.password)==True:
                # books_listed_by_seller = Book.objects.filter(sold_by = Customer.id)
                # serialized_books = BookSerialize(many=True)
                # return JsonResponse(serialized_books.data,status=201,safe=False)
                return JsonResponse('Customer Logged In',status=201,safe=False)

            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)

    # elif request.method == "POST":
    #     body_unicode = request.body.decode('utf-8')
    #     body = json.loads(body_unicode)
    #     username = body["username"]
    #     password = body['password']
    #     if Seller.objects.filter(username=username).exists():
    #         targetSeller = Seller.objects.get(username=username)
    #         if check_password(password,targetSeller.password)==True:
    #             book_id = body['id']
    #             sold_by = targetSeller
    #             name = body['name']
    #             author = body['author']
    #             new = body['new']
    #             price = body['price']

    #             newBook = Book(id=book_id,name=name,author=author,new=new,price=price,sold_by=sold_by)
    #             newBook.save()
    #             # sendotp(name,targetSeller.contact_number)

    #             books_listed_by_seller = Book.objects.filter(sold_by = targetSeller.id)
    #             serialized_books = BookSerialize(books_listed_by_seller,many=True)
    #             return JsonResponse(serialized_books.data,status=201,safe=False)

    #         else:
    #             return JsonResponse('Wrong Password',status=404,safe=False)
    #     else:
    #         return JsonResponse('User does not exist',status=401,safe=False)