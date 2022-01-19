from django.http import HttpResponse,JsonResponse
from .models import Book , Seller
from .serializers import BookSerialize ,SellerSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
import json

def home(request):
    return HttpResponse('<h1>Seller hun bhai</h1>')


def get(request):
    if request.method =="GET":
        books = Book.objects.all()
        serialized = BookSerialize(books,many=True)
        return JsonResponse(serialized.data,safe=False)

@api_view(["POST"])
def signup(request):
    if request.method=='POST':
        username = request.data['username']
        password = request.data['password']
        number = request.data['contact_number']
        hashed_password = make_password(password)
        if Seller.objects.filter(username=username).exists():
            return JsonResponse('User already exsists Try logging in',status=400,safe=False)
        newSeller = Seller(username=username,password=hashed_password,contact_number = number)
        newSeller.save()

        return JsonResponse('New User Created',status=201,safe=False)

@api_view(['GET'])
def login(request):
    if request.method == 'GET':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body["username"]
        password = body['password']
        if Seller.objects.filter(username=username).exists():
            targetSeller = Seller.objects.get(username=username)
            if check_password(password,targetSeller.password)==True:
                # return JsonResponse('Logged In',status=201,safe=False)
                books_listed_by_seller = Book.objects.filter(sold_by = targetSeller.id)
                serialized_books = BookSerialize(books_listed_by_seller,many=True)
                return JsonResponse(serialized_books.data,status=201,safe=False)

            else:
                return JsonResponse('Wrong Password',status=404,safe=False)
        else:
            return JsonResponse('User does not exist',status=401,safe=False)