from django import forms
from App_Auction.models import ProductModel


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        exclude = ['user', 'new_bidder', 'selling_price', 'status', 'created', ]
