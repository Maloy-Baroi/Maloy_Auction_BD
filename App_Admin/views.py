from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from App_Auction.models import *
from App_Authentication.models import User
import pandas as pd


# Create your views here.
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('App_Admin:admin-authentication'))

    product_price = ProductLastPrices.objects.all()
    product = ProductModel.objects.filter(status=True)
    date = []
    price = []
    for i in product_price:
        date.append(f"{i.date.day}-{i.date.month}-{i.date.year}")
        price.append(i.price)

    content = {
        'product_price': product_price,
        'date': date,
        'price': price,
        'product': product,
    }
    return render(request, 'App_Admin/admin_dashboard.html', context=content)


def admin_authentication_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        user_email = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                if is_admin(user):
                    return HttpResponseRedirect(reverse('App_Admin:admin-dashboard'))
        else:
            form = User.objects.create(email=user_email)
            form.set_password(password)
            form.save()
            user = authenticate(username=user_email, password=password)
            admin_group = Group.objects.get_or_create(name='ADMIN')
            admin_group[0].user_set.add(user)
            if user:
                login(request, user)
                if is_admin(user):
                    return HttpResponseRedirect(reverse('App_Admin:admin-dashboard'))
    return render(request, 'App_Admin/Admin_authentication.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('App_Admin:admin-authentication')


def products_gallery(request):
    products = ProductModel.objects.all()
    content = {
        'products': products
    }
    return render(request, 'App_Admin/products.html', context=content)


def running_auction(request):
    # Running Auction Statistics Start
    running_auctions = ProductModel.objects.filter(status=True)
    running_auctions_dict = {}
    for i in running_auctions:
        for j in i.product.values():
            try:
                running_auctions_dict[j['product_id']].append(j['price'])
            except KeyError:
                running_auctions_dict[j['product_id']] = ([j['price']])

    running_auctions_stat = {}
    for i, j in zip(running_auctions_dict.keys(), running_auctions_dict.values()):
        avg = sum(running_auctions_dict[i]) / len(running_auctions_dict[i])
        maximum = max(running_auctions_dict[i])
        minimum = min(running_auctions_dict[i])
        print(f"Avg: {avg}")
        print(f"Maximum: {maximum}")
        print(f"Minimum {minimum}")
        running_auctions_stat[i] = {'avg': avg, 'max': maximum, 'min': minimum}
    # Running Auction Statistics End

    content = {
        'running_auction': running_auctions,
        'running_auction_stat': zip(running_auctions_stat.keys(), running_auctions_stat.values()),
    }
    return render(request, 'App_Admin/running_auction.html', context=content)


def product_price_time_series(request, product_key):
    product_price = ProductLastPrices.objects.filter(product_id=product_key)
    price = []
    for i in product_price:
        price.append(i.price)
    content = {
        'product_price': product_price,
        'price': price
    }
    return render(request, 'App_Admin/product_price_time_series.html', context=content)


def added_ended_chart_product(request):
    product = ProductModel.objects.filter(status=True)
    content = {
        'product': product,
    }
    return render(request, 'App_Admin/added_ended_auction_chart_product.html', context=content)


def added_ended_chart(request, pk):
    product = ProductModel.objects.filter(status=True, id=pk)
    content = {
        'product': product
    }
    return render(request, 'App_Admin/added_and_ended_auction_chart.html', context=content)
