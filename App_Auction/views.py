from django.shortcuts import render, redirect
from App_Auction.models import *
from App_Auction.forms import *


# Create your views here.
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('App_Authentication:authentication')
    products = ProductModel.objects.filter(status=True)

    content = {
        'products': products
    }
    return render(request, 'home.html', context=content)
