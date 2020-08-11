from django import forms
from django.contrib.auth.models import User
from .models import Seller,Customer


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')


class SellerRegisterForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ('company_name',)


class CustomerRegisterForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('contact',)

