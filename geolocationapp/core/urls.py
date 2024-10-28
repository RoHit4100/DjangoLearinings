from django.urls import path
from .views import *

urlpatterns = [
    path('hotels/', HotelView.as_view(), name='hotelView'),
    path('hotels/<uuid:hotel_id>/', HotelView.as_view(), name='hotel_detailed'),
    path('create-user/', register, name='creater-user'),
    path('add-rating/', addRating, name='addRating'),
    path('get-rating/', getRating, name='getRating'),
]
