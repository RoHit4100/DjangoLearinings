from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rating(models.Model):
    choice = {
         (1, '1 start'),  (2, '2 start'),  (3, '3 start'),  (4, '4 start'), (5, '5 start'), 
    }
    username = models.ForeignKey(User, on_delete=models.PROTECT)
    stars = models.CharField(choices=choice)
    review = models.CharField(max_length=255)
    
class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)

    
    
    
    

 