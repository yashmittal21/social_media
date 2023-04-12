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
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 300),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


@csrf_exempt
def validateToken(request,token):
    # body = json.loads(request.body)
    # token = body['token']
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        # print(f"payload {payload}")
        return payload['user_id'] 
    except:
        return "Invalid Token"


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
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user1 = User.objects.get(id=userid)
            user2 = User.objects.get(id=id)
            user1.following += 1
            user2.follower += 1
            user1.save()
            user2.save()

            return JsonResponse({
            	"message" : "success"
            	}) 

    return JsonResponse({"message":"This is not post request"})

@csrf_exempt
def unfollow(request,id):
    if request.method == "POST":

        body = json.loads(request.body)
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user1 = User.objects.get(id=userid)
            user2 = User.objects.get(id=id)
            user1.following -= 1
            user2.follower -= 1
            user1.save()
            user2.save()
            
            return JsonResponse({
                "message" : "success"
                }) 

    return JsonResponse({"message":"This is not post request"})

def user(request):
    token = request.headers['token']
    # print(token)
    userid = validateToken(request,token)
    # print(userid)
    if userid == "Invalid Token":
        return JsonResponse({
            "message" : "Invalid token"
            })
    else:
        user = User.objects.get(id=userid)
        
        return JsonResponse({
            "message" : "success",
            "Name" : user.name,
            "follower" : user.follower,
            "following" : user.following
            })

@csrf_exempt
def posts(request):
    if request.method == "POST":

        body = json.loads(request.body)
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user = User.objects.get(id=userid)
            title = body["title"]
            description = body["description"]
            post = Post.objects.create(title=title,description=description,user=user)
            post.save()
            
            return JsonResponse({
                "message" : "success",
                "Post-Id" : post.id,
                "title" : post.title,
                "description" : post.description,
                "time" : post.time
                }) 

    return JsonResponse({"message":"This is not post request"})

@csrf_exempt
def deletePost(request,id):
    if request.method == "POST":
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user = User.objects.get(id=userid)
            post = Post.objects.get(id = id)
            post.delete();
            
            return JsonResponse({
                "message" : "Post deleted",
                })
    return JsonResponse({"message" : "This is not post request"})

@csrf_exempt
def like(request,id):
    if request.method == "POST":
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user = User.objects.get(id=userid)
            post = Post.objects.get(id = id)
            post.like += 1
            post.save()
            
            return JsonResponse({
                "message" : "Post liked",
                })
    return JsonResponse({"message" : "This is not post request"})

@csrf_exempt
def unlike(request,id):
    if request.method == "POST":
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user = User.objects.get(id=userid)
            post = Post.objects.get(id = id)
            post.like -= 1
            post.save()
            
            return JsonResponse({
                "message" : "Post unliked",
                })
    return JsonResponse({"message" : "This is not post request"})

@csrf_exempt
def comment(request,id):
    if request.method == "POST":
        token = request.headers['Token']
        # print(token)
        userid = validateToken(request,token)
        if userid == "Invalid Token":
            return JsonResponse({
                "message" : "Invalid token"
                })
        else:
            user = User.objects.get(id=userid)
            post = Post.objects.get(id = id)
            body = json.loads(request.body)
            desc = body['comment']
            comment = Comment.objects.create(desc = desc,post = post)
            comment.save()
            
            return JsonResponse({
                "comment-id" : comment.id
                })
    return JsonResponse({"message" : "This is not post request"})


def getpost(request,id):
    token = request.headers['Token']
    # print(token)
    userid = validateToken(request,token)
    if userid == "Invalid Token":
        return JsonResponse({
            "message" : "Invalid token"
            })
    else:
        user = User.objects.get(id=userid)
        post = Post.objects.get(id = id)
        comments = Comment.objects.filter(post = post).all()
        commentsDesc = []
        for c in comments:
            commentsDesc.append(c.desc)

        commentsJson = json.dumps(commentsDesc)
        print(commentsJson)

        return JsonResponse({
            "Post Id" : post.id,
            "comments" : commentsJson,
            "likes" : post.like
            })


def allpost(request):
   token = request.headers['Token']
   # print(token)
   userid = validateToken(request,token)
   if userid == "Invalid Token":
       return JsonResponse({
           "message" : "Invalid token"
           })
   else:
       user = User.objects.get(id=userid)
       posts = Post.objects.filter(user=user).all()


       postList = []


       for post in posts:


           postDict = {}
           postDict['id'] = post.id
           postDict['title'] = post.title
           postDict['desc'] = post.description
           postDict['created_at'] = post.time.isoformat()
           comments = Comment.objects.filter(post=post).all()
           desc = []
           for c in comments:
               desc.append(c.desc)
           # print(desc)
           #descJson = json.dumps(desc)
           # print(descJson)
           postDict['comments'] = desc
           postList.append(postDict)


       #postJson = json.dumps(postList)


       return JsonResponse({
           "Post" : postList,
           })
