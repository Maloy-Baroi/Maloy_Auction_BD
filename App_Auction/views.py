from django.shortcuts import render, redirect
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
            form_save.selling_price = int(minimum_price) + 1
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



