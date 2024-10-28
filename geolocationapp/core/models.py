from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class Hotel(models.Model):
    hotel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)

    class Meta:
        unique_together = (('name', 'address'),)  # This creates a unique constraint

    
class Rating(models.Model):
    STAR_CHOICES = [(i, f'{i} stars') for i in range(1, 6)]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    stars = models.IntegerField(choices=STAR_CHOICES)
    review = models.CharField(max_length=255)

    class Meta:
        unique_together = ['hotel', 'user']  # Ensures each user can only leave one rating per hotel
