from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer
from .serializers import CustomerSerialize
from rest_framework.decorators import api_view
from seller.models import Book, Seller
from seller.serializers import SellerSerializer , BookSerialize

def home(request):
    customers = Customer.objects.all()
    print(customers)
    serializedCustomer = CustomerSerialize(customers,many=True)
    # return JsonResponse(serializedCustomer.data,safe=False)
    return render(request,'customer/books.html')

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
                books = Book.objects.all()
                serialized = BookSerialize(books, many=True)
                return JsonResponse(serialized.data, safe=False)


            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)

@api_view(['POST'])
def buy(request):
    if request.method=='POST':
        body = json.loads(request.body.decode('utf-8'))
        username = body['username']
        password = body['password']
        if Customer.objects.filter(username=username).exists():
            targetCustomer = Customer.objects.get(username=username)
            print(targetCustomer.password)
            if check_password(password,targetCustomer.password)==True:
                book_name = body['book_name']
                if Book.objects.filter(name=book_name).exists():
                    targetBook = Book.objects.get(name=book_name)
                    targetCustomer.books_purchased.add(targetBook)
                    
                    Bookspurchased = targetCustomer.books_purchased
                    serializedBooks = BookSerialize(Bookspurchased,many=True)
                    return JsonResponse(serializedBooks.data,status=201,safe=False)
                else:
                    return JsonResponse('Book not found',safe=False,status=401)
            else:
                return JsonResponse("Wrong Password",safe=False,status=401)
        else:
            return JsonResponse('No User found || Try creating a new user')