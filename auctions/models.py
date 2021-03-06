from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=30)
    class Meta: 
        verbose_name_plural = "Categories"    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=75)
    description = models.CharField(null=True, max_length=1000)
    starting_price = models.DecimalField(max_digits=5, decimal_places=2)
    current_price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null= True, default=None)
    listing_active = models.BooleanField(default=True) 
    created_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="listing_images", default="listing_images/default.jpg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null= True, related_name="owner")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist_items")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null= True, related_name="buyer")

    def __str__(self):
        return f"Item: {self.title} owner: {self.owner} created: {self.created_date}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return f"{self.user} bids an amount of {self.price} on {self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2048)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"This comment was created on {self.created_date} by {self.user} : {self.content}"