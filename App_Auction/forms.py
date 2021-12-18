from django import forms
from App_Auction.models import ProductModel


class AuctionProductForm(forms.ModelForm):
    auction_end_date = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'date'}))

    class Meta:
        model = ProductModel
        exclude = ['user', 'new_bidder', 'selling_price', 'status', 'created', ]
