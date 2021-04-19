from django import forms
from django.forms import ModelForm
from . import models
from .models import Apartment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)


class ApartCreateForm(forms.ModelForm):
    class Meta:
        model = models.Apartment
        fields = (
            "name",
            "summary",
            "price",
            "house_rules",
            "roomtype",
            "status",
            "tags",
        )


class ApartUpdateForm(ModelForm):

    class Meta:
        model = Apartment
        fields = ['summary', 'price', 'status']


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')