from django.contrib.auth.forms import UserCreationForm
from home.models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter User Name'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email Address'}))
    password1=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Re Enter Passwprd'}))    
    class Meta:
        model=User
        fields={'username', 'email', 'password1', 'password2'}
