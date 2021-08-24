from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import User
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages




def index(request):
    
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "title": "ACTIVE LISTINGS",
        "users": User.objects.all()[:5]
    })

def index2(request):
    
    return render(request, "auctions/index2.html", {
        "listings": Listing.objects.all(),
        "title": "INACTIVE LISTINGS",
        "users": User.objects.all()[:5]
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



@login_required
def create_Listing(request):
    
    
    if request.method == "POST":
        user = User.objects.get(username=request.user) #get user name
        form = Create_form(request.POST, request.FILES)
        if form.is_valid():
            category = form.cleaned_data['category']
            newListing = form.save(commit=False)
            newListing.price = newListing.bids
            ## form.save(commit=False) : to bypass error if model form doesnt contains all the required field of a model
            newListing.seller = request.user
            newListing.save()
            return HttpResponseRedirect(reverse('listing_view', args=(newListing.id,)))

        else: #if form is invalid, return user to create.html
            msg_success = "Hmm... Something's Gone Wrong. Please Try Again!"
            return render(request, "auctions/create.html",{
                "form":form,
                "msg_success": msg_success,
                
               
            })
            #default view
    return render(request, "auctions/create.html",{  
        "form":Create_form()
    })









@login_required
def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all() #call and display comments on html
    user = request.user
    ###check if listing  is already in watchlist in html###
    
    watchlist = Watchlist.objects.filter(user = user)

    return render(request, "auctions/listing_view.html",{
        "listing": listing,
        "comments": comments,
        "watchlist":watchlist,
        
    })


# def seller_view(request, seller, listing_id):
#     seller = Listing.objects.filter(seller = seller)
#     listing = Listing.objects.get(pk=listing_id)
#     return render(request, 'auctions/seller_view.html',{
#         "seller": seller,
#         "listing": listing

#     })






def seller_index(request):
    listings = None ##listings has no meaningful initial value
    seller = None ## seller has no meaningful initial value
    
    if request.method == "POST":
        seller = request.POST['seller']
        listings = Listing.objects.filter(seller = seller)
    return render(request, "auctions/seller.html",{
        
        
        "listings": listings,
        "title": "Seller's Listings",
        "sellers": User.objects.all()

    })





def category_index(request):
    listings = None
    category = None
    
    if request.method == "POST":
        category = request.POST['category']
        listings = Listing.objects.filter(category = category)
    return render(request, "auctions/category.html",{
        "categories": Category.objects.all(),
        
        "listings": listings,
        "cat": "Categories",
        "sellers": User.objects.all()

    })











def add_comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(username=request.user)
    
    if request.method == "POST":
        form = Comment_form(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.user = user
            new_comment.save()
            listing.comments.add(new_comment)
            listing.save()
            comments = listing.comments.all() 
            msg = "Comment Added Successfully"
            return HttpResponseRedirect(reverse('listing_view', args=(listing.id,)))
        else:
            return render(request, "auctions/comment.html",{
                "form": form,
                "listing_id": listing.id
            })
    else:
        return render(request, "auctions/comment.html",{
            "form":Comment_form(),
            "listing_id": listing.id,

        })




def delete_comment(request):
    id=request.POST['comment_id']
    
    
    if request.method =="POST":
        comment = get_object_or_404(Comment, id=id, )
        
        
        try:
            comment.delete()
            messages.success(request, 'You have successfully deleted the comment')


        except:
                return redirect('index')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




    

def delete_listing(request, listing_id=None):  ### WORKS !!!!!
    listing = Listing.objects.get(pk=listing_id)
    if request.user == listing.seller:
        Listing.objects.filter(id=listing_id).delete()
        listings = Listing.objects.all()
        msg_success = 'You have successfully deleted listing'
        return render(request, "auctions/index.html",{
            "listings": listings,
            "msg_success": msg_success,
            "listing": listing   
            })
        
    else:
        msg_error = "Hold on a second ! Only the seller of the Listing or Admin can delete listing"
        listings = Listing.objects.all()
        return render(request, "auctions/index.html",{
            "listings": listings,
            "msg_error": msg_error,
            "listing": listing   
            })
    


def category_index(request):
    listings = None
    category = None
    
    if request.method == "POST":
        category = request.POST['category']
        listings = Listing.objects.filter(category = category)
    return render(request, "auctions/category.html",{
        "categories": Category.objects.all(),
        
        "listings": listings,
        "cat": "Categories",
        "sellers": User.objects.all()

    })



    
# def watchlist(request):
#     viewers = Viewer.objects.all()
#     if request.user.id is None:
#         return redirect('index')

#     my_watchlist = Watchlist.objects.get(user=request.user)
#     totalAuctions = my_watchlist.auctions.count()
#     context = {
#         'my_watchlist': my_watchlist,
#         'viewers': viewers,
#         'totalAuctions': totalAuctions, 
#     }
#     return render(request, "auctions/watchlist.html", context)


def test(request):
    return render (request, 'auctions/test.html')


@login_required   
def listing_remove(request):

    id = request.POST['listing_id']

    if request.method =="POST":
        listing = get_object_or_404(Listing, id=id, )

        try:
            listing.delete()
        
        except:
            return redirect('index')

    delete_success = 'Listing Deleted!'
    return render(request, "auctions/index.html",{
        "delete_success":delete_success
    })




@login_required
def watchlist(request):
    
    user = request.user
    watchlist = Watchlist.objects.filter(user = user)
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })



def watchlist_add_remove(request, listing_id):
    user = request.user
    listing = Listing.objects.filter(id = listing_id).first()
    watchlist = Watchlist.objects.filter(user = user, listing = listing).first()

    if watchlist is None:
        newlist = Watchlist.objects.create(user=user, listing = listing)

        newlist.save()


    
        return render(request, "auctions/watchlist.html", {
        "watchlist": Watchlist.objects.filter(user = user),
        "watchlist_add_msg": "Listing Added",
        "listing": Listing.objects.get(pk=listing_id)
        })

    else:
        watchlist.delete()

    
    return render(request, "auctions/index.html",{
            "listings" : Listing.objects.all(),
            "watchlist_remove": 'You have successfully removed listing from Watchlist',
            "listing": Listing.objects.get(pk=listing_id)
            
            })
        





def listing_close(request, listing):
    if request.method == 'GET':
        auction = Listing.objects.get(id=listing)
        auction.close_listing = True
        auction.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def listing_unclose(request, listing):
    if request.method == 'GET':
        auction = Listing.objects.get(id=listing)
        auction.close_listing = False
        auction.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def new_bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    highest_bid = listing.price
    bForm = Bid_form(request.POST or None)
    
    if request.method == "GET":
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
      
    
    elif request.method =="POST":
        
        if bForm.is_valid():
            bForm = bForm.save(commit=False)
            if bForm.price >= listing.bids and bForm.price > highest_bid:
                highest_bid = bForm.price
                listing.bid_winner = request.user.username
                listing.price = highest_bid
                listing.save()
            else:
                messages.error(request, "Please place a higher bid than the current price / currently highest bid")
                return HttpResponseRedirect(request.session['login_from'])
            
            bForm.listing = listing
            bForm.user = request.user
            
            bForm.save()
            messages.success(request, "Bid successful")
            return HttpResponseRedirect(reverse('listing_view', args=(listing.id,)))
    return render(request, "auctions/bidding.html", {
        "bForm": bForm,
        "highest_bid": listing.price
    })


@login_required
def mybids(request):
    
    user = request.user
    mybids = Bid.objects.filter(user = user)
    
    return render(request, "auctions/bidlist.html", {
        "mybids": mybids
    })


def view_bids(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/view_bids.html", {
        'listing': listing,
    })