from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("details/<int:listing_id>", views.listingdetails, name="details"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("addlist/<int:listing_id>", views.addlist, name="addlist"),
    path("removelist/<int:listing_id>", views.removelist, name="removelist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("all", views.all, name="all")
]

