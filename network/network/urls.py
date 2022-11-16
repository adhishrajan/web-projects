
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("details/<str:username>", views.details, name="details"),
    path("follow/<str:username>", views.follow, name='follow'),
    path("unfollow/<str:username>", views.unfollow, name='unfollow'),
    path("dne", views.details, name="dne"),
    path("following/<str:username>", views.following, name="following"),
    path("users", views.users, name="users"),

    #API Routes
    path("edit/<str:postid>", views.edit, name="edit"), 
    path("like/<str:postid>", views.like, name="like")
]
