from django.forms import ModelForm, Textarea
from .models import User, Listing, Category, Bid
from django import forms

class Create_new_listingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_price', 'category', 'image']
        widgets = {
            'description': Textarea(attrs={'col-md': 8, 'col-lg': 10, 'rows' : 10})
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid 
        fields = ['price']