from django.shortcuts import render
import json
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer
from .serializers import CustomerSerialize
from rest_framework.decorators import api_view
from seller.models import Book, Seller
from seller.serializers import SellerSerializer , BookSerialize
import random

def home(request):
    customers = Customer.objects.all()
    print(customers)
    serializedCustomer = CustomerSerialize(customers,many=True)
    # return JsonResponse(serializedCustomer.data,safe=False)
    return render(request,'customer/allcustomers.html',context={'customers':serializedCustomer.data})

@api_view(['GET','POST'])
def signup(request):
    if request.method == 'GET':
        return render(request,'customer/signup.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        number = request.POST.get('number')
        if Customer.objects.filter(username=username).exists():
            return JsonResponse('User Already Exists || Try login',status=400,safe=False)
        
        newCustomer = Customer(username=username,password=make_password(password),contact_number=number)
        newCustomer.save()

        return render(request, 'customer/login.html')

@api_view(['GET','POST'])
def login(request):
    if request.method == 'GET':
        # print(request.body)
        return render(request, 'customer/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Customer.objects.filter(username=username).exists():
            targetCustomer = Customer.objects.get(username=username)
            if check_password(password,targetCustomer.password)==True:
                books = targetCustomer.books_purchased
                serialized = BookSerialize(books, many=True)
                # return JsonResponse(serialized.data, safe=False)
                return render(request, 'customer/books.html',context={'books':serialized.data})


            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)

@api_view(['POST','GET'])
def buy(request):
    if request.method=='POST':
        # body = json.loads(request.body.decode('utf-8'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Customer.objects.filter(username=username).exists():
            targetCustomer = Customer.objects.get(username=username)
            print(targetCustomer.password)
            if check_password(password,targetCustomer.password)==True:
                book_name = request.POST.get('book_name')
                if Book.objects.filter(name=book_name).exists():

                    generatedOtp = random.randint(1999,9999)
                    targetCustomer.otp = generatedOtp
                    targetCustomer.save()
                    
                    request.session['book']=book_name
                    request.session['hello'] = 'hellop'
                    
                    return render(request,'customer/otp.html')

                else:
                    return JsonResponse('Book not found',safe=False,status=401)
            else:
                return JsonResponse("Wrong Password",safe=False,status=401)
        else:
            return JsonResponse('No User found || Try creating a new user',safe=False,status=401)
    elif request.method == 'GET':
        books = Book.objects.all()
        serializedBooks = BookSerialize(books,many=True)
        return render(request,'customer/buy.html',context={'books':serializedBooks.data})
@api_view(['POST'])
def otpVerify(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        otp_provided = request.POST.get('otp')
        if Customer.objects.filter(username=username).exists():
            targetCustomer = Customer.objects.get(username=username)
            print(targetCustomer.otp)
            print(otp_provided)
            if int(otp_provided) == targetCustomer.otp:
                if 'book' in request.session:
                    book_name = request.session.get('book')
                    targetBook = Book.objects.get(name=book_name)
                    del request.session['book']
                    targetCustomer.books_purchased.add(targetBook)
                    
                    Bookspurchased = targetCustomer.books_purchased
                    serializedBooks = BookSerialize(Bookspurchased,many=True)
                    return render(request, 'customer/books.html',context={'books':serializedBooks.data})
                else:
                    return JsonResponse('Book not found',safe=False,status=401)
            else:
                return JsonResponse('Otp not matched',safe=False,status=401)
        else:
            return JsonResponse('User not exists',safe=False,status=401)