from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=30)
    class Meta: 
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(null=True, max_length=500)
    starting_price = models.FloatField()
    current_price = models.FloatField(blank=True, null= True)
    listing_active = models.BooleanField(default=True) 
    created_date = models.DateTimeField(auto_now=True)
    image = models.URLField(default="http://127.0.0.1:8000/static/auctions/default.jpg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null= True)
 
    def __str__(self):
        return f"{self.title}"
