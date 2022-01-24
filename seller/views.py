from django.http import HttpResponse,JsonResponse
from .models import Book , Seller
from .serializers import BookSerialize ,SellerSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
import json
from twilio.rest import Client
from django.shortcuts import render

def home(request):
    return HttpResponse('<h1>Seller hun bhai</h1>')


def get(request):
    if request.method =="GET":
        books = Book.objects.all()
        serialized = BookSerialize(books,many=True)
        return JsonResponse(serialized.data,safe=False)

@api_view(["POST",'GET'])
def signup(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        number = request.POST.get('contact_number')
        hashed_password = make_password(password)
        if Seller.objects.filter(username=username).exists():
            return JsonResponse('Seller already exsists Try logging in',status=400,safe=False)
        newSeller = Seller(username=username,password=hashed_password,contact_number = number)
        newSeller.save()

        return JsonResponse('New User Created',status=201,safe=False)
    elif request.method == 'GET':
        return render(request, 'seller/Signup.html',)

@api_view(['GET','POST'])
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Seller.objects.filter(username=username).exists():
            targetSeller = Seller.objects.get(username=username)
            if check_password(password,targetSeller.password)==True:
                books_listed_by_seller = Book.objects.filter(sold_by = targetSeller.id)
                serialized_books = BookSerialize(books_listed_by_seller,many=True)
                # return JsonResponse(serialized_books.data,status=201,safe=False)
                return render(request,'seller/books.html',context={'books':serialized_books.data})

            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)
    elif request.method == 'GET':
        return render(request,'seller/login.html',)

def sell(request):
    if request.method == "POST":
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Seller.objects.filter(username=username).exists():
            targetSeller = Seller.objects.get(username=username)
            if check_password(password,targetSeller.password)==True:
                book_id = request.POST.get('id')
                # sold_by.add(targetSeller)
                name = request.POST.get('name')
                author = request.POST.get('author')
                new = True
                price = request.POST.get('price')

                newBook = Book(id=book_id,name=name,author=author,new=new,price=price)
                newBook.save()
                newBook.sold_by.add(targetSeller)
                # sendotp(name,targetSeller.contact_number)

                books_listed_by_seller = Book.objects.filter(sold_by = targetSeller.id)
                serialized_books = BookSerialize(books_listed_by_seller,many=True)
                # return JsonResponse(serialized_books.data,status=201,safe=False)
                return render(request,'seller/books.html',context={'books':serialized_books.data})

            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)

    elif request.method == 'GET':
        return render(request, 'seller/sell.html')



# def sendotp(product, number):
#     account_sid = "="
#     auth_token = "="
#     client = Client(account_sid, auth_token)
#     # try:
#     message = client.messages \
#                 .create(
#                         body="Your Book : {} has been listed on our book store. Thank you".format(product),
#                         from_="+19377447720",
#                         to="+91{}".format(number),
#                     )

#     # print(message.sid)
#     print(message)
    # except Exception as ex:
    #     print(ex)