from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect

# Create your views here.
from App_Admin.views import is_admin
from App_Authentication.forms import SignUpForm, ProfileForms
from App_Authentication.models import User, Profile


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
                elif is_admin(user):
                    return HttpResponseRedirect(reverse('App_Admin:admin-dashboard'))
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


@login_required
@user_passes_test(is_customer)
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    profileForm = ProfileForms(instance=request.user)
    if request.method == 'POST':
        profileForm = ProfileForms(data=request.POST, instance=request.user)
        if profileForm.is_valid():
            form = profileForm.save(commit=False)
            form.user = request.user
            form.save()

    content = {
        'form': profileForm,
        'profile': profile
    }
    return render(request, 'App_Authentication/profile.html', context=content)
