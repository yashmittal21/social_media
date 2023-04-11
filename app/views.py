from django.shortcuts import render, HttpResponse
import jwt, datetime
from rest_framework import exceptions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from django.contrib.auth.hashers import make_password,  check_password
# Create your views here.

@csrf_exempt
def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 60),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


@csrf_exempt
def validateToken(request):
    body = json.loads(request.body)
    token = body['token']
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')

        return JsonResponse({
            "message" : True
        })
    except:
        return JsonResponse({
            "message" : False
        })


@csrf_exempt
def authenticate(request):
    if request.method == "POST":
        body = json.loads(request.body)
        print(body)
        email = body["email"]
        password = body["password"]
        #print(password)

        #print(encryptedPassword)

        if not User.objects.filter(email = email, password=password).exists():
            #print("here")
            return JsonResponse({
                "message" : "Failed",
                "error" : "Invalid Credantial"
            })

        user = User.objects.filter(email = email)[0]

        
        accessToekn = create_access_token(user.id)

        return JsonResponse({
            "messgae" : "success",
            "token" : accessToekn,
            "userId" : user.id,
            # "type" : type
        })
        
    return JsonResponse({"message":"This is not post request"})

@csrf_exempt
def follow(request,id):
	if request.method == "POST":
		body = json.loads(request.body)
		print(body)

		return JsonResponse({
			"message" : "success"
			}) 