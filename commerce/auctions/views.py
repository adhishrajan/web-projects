from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Comment, Lis, Bids, Watchlist, ClosedLis, AllLis
from datetime import datetime


def index(request):
    #View for home page (active listings)
    listings = Lis.objects.all()
    empty = False
    if len(listings) == 0:
        empty = True
    return render(request, "auctions/index.html", {
        "listings": listings,
        "empty": empty
    })


def all(request):
    #View for all listings
    listings = AllLis.objects.all()
    empty = False
    if len(listings) == 0:
        empty = True
    return render(request, "auctions/alllist.html", {
        "listings": listings,
        "empty": empty
    })


def categories(request):
    #View for category page
    #Raw SQL Command to group lis database by category
    catsort = Lis.objects.raw("SELECT * FROM auctions_lis GROUP BY category")
    return render(request, "auctions/categories.html", {
        "catsort": catsort
    })


def category(request, category):
    #View for each individual category
    c = Lis.objects.filter(category=category)
    empty = False
    if len(c) == 0:
        empty = True
    return render(request, "auctions/cat.html", {
        "empty": empty,
        "c": c,
        "category": category

    })

@login_required
    #View to display comments   
def comments(request, listing_id):
    if request.method == "POST":
        com = Comment()
        com.comment = request.POST.get('comments')
        com.user = request.user.username
        com.listing_id = listing_id
        com.save(Comment)
        return redirect('details', listing_id)
    else :
        return redirect('index')




@login_required
def removelist(request, listing_id):
    #View to remove items from watchlist
    if request.user.username:
        #Get the listing from the watchlist and delete
        watchL = Watchlist.objects.get(user=request.user, listing_id=listing_id)
        watchL.delete()
        return redirect('watchlist')
    else:
        return redirect('index')



@login_required
def create_listing(request): 
    #View to create a listings
    if request.method == "POST":
        #Assigning data from the form to the Lis model
        list1 = Lis()
        list1.owner = request.user.username
        list1.name = request.POST.get('name')
        list1.description = request.POST.get('description')
        list1.category = request.POST.get('category')
        list1.price = request.POST.get('price')
        if request.POST.get('img'):
            list1.img = request.POST.get('img')
        else:
            list1.img = "https://www.justadviser.com/staticcontent/globalassets/just-adviser/rebrand-assets/download/404_robot_optb.gif"
        list1.save(Lis)
        #Assigning data from the form to the Alllis model
        listings = Lis.objects.all()
        list2 = AllLis()
        list2.owner = request.user.username
        list2.name = request.POST.get('name')
        list2.description = request.POST.get('description')
        list2.category = request.POST.get('category')
        list2.price = request.POST.get('price')
        if request.POST.get('img'):
            list2.img = request.POST.get('img')
        else:
            list2.img = "https://www.justadviser.com/staticcontent/globalassets/just-adviser/rebrand-assets/download/404_robot_optb.gif"
        list2.save(AllLis)
    else: 
        return render(request, "auctions/create_listing.html")
    return render(request, "auctions/index.html", {
        "listings": listings,
        "user": list1.owner
    })
        

    
@login_required
def bid(request, listing_id):
    #View for submitting a bid
    bid = Lis.objects.get(id=listing_id)
    bid = bid.price
    if request.method == "POST":
        newbid = int(request.POST.get("bid"))
        if newbid > bid:
            #if the new bid is greater than current bid, save it into Bid model
            ling1 = AllLis.objects.get(id=listing_id)
            ling1.price = newbid
            ling1.save()
            ling = Lis.objects.get(id=listing_id)
            ling.price = newbid
            ling.save()
            try:
                if Bids.objects.filter(id=listing_id):
                    bid1 = Bids.objects.filter(id=listing_id)
                    bid1.delete()
                bids = Bids()
                bids.user = request.user.username
                bids.name = ling.name
                bids.listing_id = listing_id
                bids.bid = newbid
                bids.save()      
            except:
                bids = Bids()
                bids.user = request.user.username
                bids.name = ling.name
                bids.listing_id = listing_id
                bids.bid = newbid
                bids.save()
            #Setting two cookies that displays success and error messages
            cookie = redirect('details', listing_id)
            cookie.set_cookie('success','You have successfully bid on this item!', max_age = 5)
            return cookie
        else :
            cookie = redirect('details', listing_id)
            cookie.set_cookie('wrong','Bid unsuccessful: bid must be greater than current bid', max_age = 5)
            return cookie
     
    else:
        return redirect('index')


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def watchlist(request):
    #View for users watchlist page
    if request.user.username:
        try:
            #Add every listing that is on the watchlist model to a new list (called filtered)
            userwatch = Watchlist.objects.filter(user=request.user.username)
            filtered = []
            for liswatch in userwatch:
                filtered.append(AllLis.objects.filter(id=liswatch.listing_id))
            try:
                userwatch = Watchlist.objects.filter(user=request.user.username)
                watchamnt= len(userwatch)
                empty = False
            except:
                watchamnt = None
                empty = True
            return render(request,"auctions/watchlist.html",{
                "list": filtered,
                "watchamnt":watchamnt,
                "empty": empty
            })
        except:
            try:
                qwuser = Watchlist.objects.filter(user=request.user.username)
                watchamnt =len(qwuser)
            except:
                watchamnt = None
            return render(request,"auctions/watchlist.html",{
                "list": None,
                "watchamnt": watchamnt
            })
    else:
        return redirect('index')


@login_required
def addlist(request, listing_id):
    #View to add a listing to a user's watchlist
    if request.user.username:
        watchL = Watchlist()
        watchL.user = request.user.username
        watchL.listing_id = listing_id
        watchL.save()
        return redirect('watchlist')
    else:
        return redirect('index')


def listingdetails(request, listing_id):
    #View to display the listing's details
    ling = AllLis.objects.get(id=listing_id)
    if request.user.username:
        try:
            #If the listing is already on a user's watchlist
            if Watchlist.objects.get(user=request.user, listing_id=listing_id):
                watched=True
        except:
            watched = False
        try:
            #If there are comments already displayed for that listings
            coms = Comment.objects.filter(listing_id=listing_id)
        except:
            coms = None
        try:
            b = Bids.objects.filter(listing_id=listing_id)
            bidamnt = len(b)
        except:
            b = None
        try:
           winn = Bids.objects.get(listing_id=listing_id, bid=ling.price)
        except:
            winn = None
        try:
            #If the listing is active, return its details
            if Lis.objects.get(id=listing_id):
                return render(request, "auctions/listingdetails.html", {
                    "ling": ling, 
                    "watched": watched,
                    "wrong": request.COOKIES.get('wrong'),
                    "success": request.COOKIES.get('success'),
                    "coms": coms,
                    "bidamnt": bidamnt,
                    "winn": winn
                })
            #If the listing is no longer active, return the win page (which will display who won the bid)
            else:
                return render(request, "auctions/win.html")
        except:
            a = ClosedLis.objects.get(listing_id=listing_id)
            return render(request, "auctions/win.html", {
                "a": a
            })
    else:
        watched = False
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        watchamnt = len(w)
    except:
        watchamnt = None
    return render(request, "auctions/listingdetails.html", {
        "ling": ling, 
        "watchamnt": watchamnt,
        "watched": watched,
        "wrong": request.COOKIES.get('wrong'),
        "success": request.COOKIES.get('success'),
        "coms": coms,
        "bidamnt": bidamnt,
        "winn": winn
    })


@login_required
def close(request, listing_id):
    #View for closing the bid and making the listing no longer active
    ling = Lis.objects.get(id=listing_id)
    if request.user.username:
        #Adding the listing details to the ClosedLis model
        closed = ClosedLis()
        closed.name = ling.name
        closed.owner = ling.owner
        closed.listing_id = listing_id
        try:
            #Assigning the highest bid to the winprice of the ClosedLis
            bidd = Bids.objects.get(listing_id=listing_id, bid=ling.price)
            closed.winner = bidd.user
            closed.winprice = bidd.bid 
            closed.save()
            bidd.delete()
        except:
            closed.winner = ling.owner
            closed.winprice = ling.price
            closed.save()
        try:
            #Deleting all comments and watchlists
            if Watchlist.objects.filter(listing_id=listing_id):
                wa = Watchlist.objects.filter(listing_id=listing_id)
                wa.delete()
            else:
                pass
        except:
            pass
        try:
            co = Comment.objects.filter(listing_id=listing_id)
            co.delete()
        except:
            pass
        try:
            bid1 = Bid.objects.filter(listing_id=listing_id)
            bid1.delete()
        except:
            pass
        try:
            a = ClosedLis.objects.get(listing_id=listing_id)
            ling.delete()
        except:
            closed.owner = ling.owner
            closed.winner = ling.owner
            closed.listing_id = listing_id
            closed.winprice = ling.price
            closed.save()
            a = ClosedLis.objects.get(listing_id=listing_id)
            ling.delete()
        try:
            li = Watchlist.objects.filter(user=request.user.username)
            x = len(li)
        except:
            x = None
        return render(request,"auctions/win.html",{
            "a": a,
            "wcount": x
        })   

    else:
        return redirect('index')     

