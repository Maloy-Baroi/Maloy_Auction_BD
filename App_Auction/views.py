import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from App_Auction.models import *
from App_Auction.forms import *


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('App_Authentication:authentication')
    products = ProductModel.objects.filter(status=True).order_by('-created')

    form = AuctionProductForm()
    if request.method == 'POST':
        form = AuctionProductForm(request.POST, request.FILES)
        if form.is_valid():
            minimum_price = request.POST.get('minimum_bid_price')
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.status = True
            form_save.save()
            print(f"New product ID: {form_save.pk}")
            bid_price_list = ProductLastPrices(product_id=form_save.pk, price=minimum_price)
            bid_price_list.save()
            return redirect('home')
    content = {
        'products': products,
        'form': form
    }
    return render(request, 'home.html', context=content)


def product_details_view(request, product_key):
    product = ProductModel.objects.get(id=product_key)
    print(product)
    bidding_table = ProductLastPrices.objects.all().filter(product_id=product_key)
    bidder = False
    min_bid_price = product.minimum_bid_price
    try:
        bidder_exists = ProductLastPrices.objects.get(product=product, bidder=request.user)
        if bidder_exists:
            bidder = True
            min_bid_price = bidder_exists.price
    except:
        bidder = False

    # Date
    today = datetime.datetime.today().date()
    # Date End
    # Product Bidding Date Ended or not (Start)
    winner = None
    if product.auction_end_date < today:
        product.status = False
        max_price = max([i.price for i in bidding_table.order_by('date')])
        winner_list = [i for i in bidding_table if i.price == max_price]
        old_date = min([i.date for i in winner_list])
        winner = [i for i in winner_list if i.date == old_date]

    # Product Bidding Date Ended or not (End)

    if not product.status:
        timeup = True
    else:
        timeup = False
    content = {
        'product': product,
        'bidding_table': bidding_table,
        'bidder_exist': bidder,
        'min_bid_price': min_bid_price,
        'timeup': timeup,
        'winner': winner
    }

    return render(request, 'App_Auction/product_details.html', context=content)


def bid_start_view(request):
    if request.method == 'POST':
        product_key = request.POST.get('product_key')
        bid_price = request.POST.get('bid_price')
        product = ProductModel.objects.get(id=product_key)
        if request.user == product.user:
            messages.error(request, "You are the auction owner, You can't bid")
            return HttpResponseRedirect(reverse('App_Auction:product-details', kwargs={'product_key': product_key}))
        try:
            bidder_exists = ProductLastPrices.objects.get(product=product, bidder=request.user)
            bidder_exists.price = bid_price
            bidder_exists.save()
        except:
            newBid = ProductLastPrices.objects.create(product=product, bidder=request.user, price=int(bid_price))
            newBid.save()
        return HttpResponseRedirect(reverse('App_Auction:product-details', kwargs={'product_key': product_key}))
