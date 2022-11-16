from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import EditPageForm
import json
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Post, Like, Follower
from django.core.paginator import Paginator



def index(request):
     #View for home page
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    empty = False
    if len(posts) == 0:
        empty = True
    return render(request, "network/index.html", {
        "posts": posts,
        "empty": empty,
        'page_obj': page_obj
    })



def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    #View to log user out
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")






@login_required
def new(request): 
    #View to create a post
    if request.method == "POST":
        #Assigning data from the form to the Post model
        post1 = Post()
        post1.user = request.user.username
        post1.body = request.POST.get('body')
        post1.save(Post)
        posts = Post.objects.all()
    else: 
        return render(request, "network/new.html")
    return redirect('index')



def users(request):
    #View for list of all users
    users = User.objects.all()
    return render(request, "network/users.html",{
        "users": users
    })



@login_required
def following(request, username):
    #View of posts made by users that the user follows
    user = User.objects.get(username=request.user.username)    
    followings = Follower.objects.filter(follower=user)
    postss = []
    for f in followings:
        posts = Post.objects.filter(user=f.following)
        for post in posts:
            post.likes = len(Like.objects.filter(body=post.id))
            post.save()
            postss.append(post)
    if len(postss) == 0:
        empty = True
    else:
        empty = False
    paginator = Paginator(postss, 10) # Show 10 contacts per page.   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": postss,
        "page_obj": page_obj,
        "empty": empty
    })



#View for profile page
def details(request, username):
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).order_by('-timestamp')
        paginator = Paginator(posts, 10) # Show 10 contacts per page.   
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        followings = user.following.all()
        followers = user.followers.all()
        folcount = len(followers)
        postcount = len(posts)
        folingcount = len(followings)
        followed = False
        empty = True
        if len(posts) > 0:
            empty = False
        for fer in followers:
            if request.user.username == fer.follower.username:
                followed = True
    except ObjectDoesNotExist:
        return render(request, "network/dne.html")
    return render(request, "network/details.html", {
        "username": username,
        "posts": posts,
        "followings": followings,
        "followers": followers,
        "followed": followed,
        "folcount": folcount,
        "postcount": postcount,
        "folingcount": folingcount,
        "empty": empty,
        "page_obj": page_obj
    })
    



def unfollow(request, username):
    user = User.objects.get(username=username)
    request.user.unfollow(user)
    return redirect('details', username)



def follow(request, username):
    user = User.objects.get(username=username)
    request.user.follow(user)
    return redirect('details', username)


#View to save edited post body into post object
@csrf_exempt
def edit(request, postid):
    post = Post.objects.get(id=postid)
    
    if request.method == "PUT":
        received_json_data = json.loads(request.body.decode("utf-8"))
        post.body = received_json_data["body"]
        post.save()
        return HttpResponse(status=204)



#View to like a post
@csrf_exempt
def like(request, postid):

    post = Post.objects.get(id=postid)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "PUT":
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data["like"])
        if received_json_data["like"]:
            Like.objects.create(user=request.user, body=post)
            post.likes = len(Like.objects.filter(body=post))
        else:
            Like.objects.filter(user=request.user, body=post).delete()
            post.likes = len(Like.objects.filter(body=post))
        post.save()
        return HttpResponse(status=204)