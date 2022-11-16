from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("quizlist", views.quizlist, name="quizlist"),
    path("newquiz", views.newquiz, name="newquiz"),
    path("follow/<str:username>", views.follow, name='follow'),
    path("unfollow/<str:username>", views.unfollow, name='unfollow'),
    path("taken/<str:username>", views.taken, name='taken'),
    path("following/<str:username>", views.following, name='following'),
    path("myquizzes/<str:username>", views.myquizzes, name="myquizzes"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:quiz_pk>", views.quiz_view, name="quiz_view"),
    path("<int:quiz_pk>/quiz_viewcont", views.quiz_viewcont, name="quiz_viewcont"),
    path("<int:quiz_pk>/save", views.save, name="save"),


]

