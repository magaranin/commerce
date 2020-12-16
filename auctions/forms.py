from django.forms import ModelForm, Textarea
from .models import User, Listing, Category, Bid, Comment
from django import forms

class Create_new_listingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_price', 'category', 'image']
        widgets = {
            'title':Textarea(attrs={'class': 'form-control', 'rows' : 1}),
            'description': Textarea(attrs={'class': 'form-control', 'rows' : 2}),
        }
 

class BidForm(ModelForm):
    class Meta:
        model = Bid 
        fields = ['price']
        labels = {
            'price': ''
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows' : 2}
        )}
        labels = {
            'content': 'Comment'
        }
