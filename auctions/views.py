from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm


from .models import User, Listing, Category
from .forms import create_new_listingForm
from django.contrib.auth.decorators import login_required



def index(request):
    select_cat=int(request.GET.get('category_id', -1))
    if select_cat >= 1:
        listings = Listing.objects.filter(category__id=select_cat)
    else:
        listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings 
        #"title": "Active Listings"
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

def listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    is_watched = user.watchlist_items.filter(pk=listing_id).exists()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched
    })

@login_required
def create_new_listing(request):
    if request.method == "POST":
        form = create_new_listingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing = form.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': new_listing.id}))
    else:
        return render(request, "auctions/create_new_listing.html", {
        "form": create_new_listingForm()
    })

def categories(request):
    return render(request,"auctions/categories.html", {
        "categories": Category.objects.all()
    })

@login_required
def update_watchlist(request, listing_id):
    if request.method == "POST": 
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        if user.watchlist_items.filter(pk=listing_id).exists():
            user.watchlist_items.remove(listing)
        else:
            user.watchlist_items.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
    user = request.user
    return render(request, "auctions/index.html", {
        "listings": user.watchlist_items.all()
    })