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
    title = models.CharField(max_length=64)
    description = models.CharField(null=True, max_length=2048)
    starting_price = models.FloatField()
    current_price = models.FloatField(blank=True, null= True)
    listing_active = models.BooleanField(default=True) 
    created_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="listing_images", default="listing_images/default.jpg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist_items")
    def __str__(self):
        return f"Item: {self.title} owner: {self.owner} created: {self.created_date}"


