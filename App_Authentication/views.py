from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect

# Create your views here.
from App_Authentication.forms import SignUpForm
from App_Authentication.models import User


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def authentication_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        user_email = request.POST.get('username')
        password = request.POST.get('password')
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=user_email, password=password)
            if user:
                login(request, user)
                if is_customer(user):
                    return HttpResponseRedirect(reverse('home'))
        else:
            form = User.objects.create(email=user_email)
            form.set_password(password)
            form.save()
            user = authenticate(username=user_email, password=password)
            customer_grp = Group.objects.get_or_create(name='CUSTOMER')
            customer_grp[0].user_set.add(user)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
    return render(request, 'App_Authentication/authentication.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('App_Authentication:authentication')
