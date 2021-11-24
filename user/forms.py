from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    '''
        This form is to provide the similar admin interface to the CustomUser as User(build-in).
    '''
    class Meta:
        model = CustomUser
        fields = '__all__'