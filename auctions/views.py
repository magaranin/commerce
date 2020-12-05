from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelForm


from .models import User, Listing, Category, Bid
from .forms import Create_new_listingForm, BidForm
from django.contrib.auth.decorators import login_required



def index(request):
    select_cat=int(request.GET.get('category_id', -1))
    if select_cat >= 1:
        listings = Listing.objects.filter(category__id=select_cat).filter(listing_active=True)
    else:
        listings = Listing.objects.filter(listing_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings 
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
    can_close = listing.listing_active == True and request.user == listing.owner
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watched": is_watched,
        "can_close": can_close,
        "form": BidForm()
    })

@login_required
def create_new_listing(request):
    if request.method == "POST":
        form = Create_new_listingForm(request.POST, request.FILES)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.owner = request.user
            new_listing = form.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': new_listing.id}))
    else:
        return render(request, "auctions/create_new_listing.html", {
            "form": Create_new_listingForm()
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

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data["price"]
            listing = Listing.objects.get(pk=listing_id)
            current_price = listing.current_price
            start_price = listing.starting_price
            if price < start_price:
                user = request.user
                is_watched = user.watchlist_items.filter(pk=listing_id).exists()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "is_watched": is_watched,
                    "form": form,
                    "message": "Bid can't be less than asking price!" 
                    }) 
            if (current_price is None and price >= start_price) or price > current_price:
                    bid = form.save(commit=False)
                    user = request.user
                    bid.user = user
                    bid.listing = listing
                    bid = form.save()
                    listing.current_price = price
                    listing.save()
                    is_watched = user.watchlist_items.filter(pk=listing_id).exists()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "is_watched": is_watched,
                        "form": BidForm(),
                        "message": "Bid successfully placed!"
                        })
            else:
                user = request.user
                is_watched = user.watchlist_items.filter(pk=listing_id).exists()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "is_watched": is_watched,
                    "form": form,
                    "message": "Price can't be less or equal to the previous bid!" 
                    })
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    

@login_required
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id) 
        if  listing.listing_active == True and request.user == listing.owner:
            if listing.current_price is None:
                listing.listing_active = False
                listing.save() 
                return render(request, "auctions/listing.html", {
                    "listing": listing, 
                    })
            else:    
                listing.buyer = Bid.objects.filter(listing=listing).last().user            
                listing.listing_active = False
                listing.save()           
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                })        
    return HttpResponseRedirect(reverse("listing page", args=(listing_id,)))    
        



