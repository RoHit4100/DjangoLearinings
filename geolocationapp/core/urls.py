from django.urls import path
from . import views

urlpatterns = [
    path('createRestaurant/', views.createRestaurant, name='createRestaurant'),
]
