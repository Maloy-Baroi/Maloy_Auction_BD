from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from App_Authentication.models import User, Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class ProfileForms(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
