from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from django.contrib.auth.models import User
from .models import Hotel, Rating
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class HotelView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            name = data.get('name')
            address = data.get('address')

            if not name or not address:
                return JsonResponse({'error': 'missing values'}, status=400)
            
            Hotel.objects.create(name=name, address=address)
            return JsonResponse({'message': 'Successfully created hotel'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    def get(self, request):
        try:
            hotels = Hotel.objects.all().values()
            return JsonResponse(list(hotels), safe=False, status=200)
        except Exception as e: 
            return JsonResponse({'error': str(e)}, status=400)
                
    # for patch
    def patch(self, request, hotel_id):
        if not hotel_id:
            return JsonResponse({"error": "hotel id is required"}, status=400)
        return self.updateHotel(request, hotel_id)
    
    # for put
    def put(self, request, hotel_id):
        return self.updateHotel(request, hotel_id)
    
    def delete(self, request, hotel_id):
        try:
           hotel = Hotel.objects.get(hotel_id=hotel_id)
           hotel.delete()
           return JsonResponse({'message': 'hotel successfully deleted'}, status=200)
        except Hotel.DoesNotExist:
            return JsonResponse({'error': 'There is no hotel with this id'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    
    def updateHotel(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(hotel_id=hotel_id)
            data = json.loads(request.body)
            name = data.get('name')
            address = data.get('address')
            
            if name:
                hotel.name = name
            if address:
                hotel.address = address

            hotel.save()
            return JsonResponse({'message': 'booking succesfully updated'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            

@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            # get the required fields 
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            if not username or not email or not password:
                return JsonResponse({'error': 'Missing values'}, status=400) 
            
            User.objects.create_user(username=username, email=email, password=password)
            return JsonResponse({'message': 'user successfully created'}, status=200)
        else:
            return JsonResponse({'error': 'only Post method is allowed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

@csrf_exempt    
def addRating(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            hotel_id = data.get('hotel_id')
            # first check if there is any hotel with the same id or not
            hotel = Hotel.objects.get(hotel_id=hotel_id)
            if not hotel:
                return JsonResponse({'error': 'There is not hotel with this id'}, status=400)
            
            stars = data.get('stars')
            review = data.get('review')
            username = request.username
            # check if the username exists in the user table or not
            user = User.objects.get(username=username)
            if not stars or not review:
                return JsonResponse({'error': 'Missing values'}, status=200)
            
            rating = Rating.objects.create(
                hotel=hotel,
                user=user, 
                stars=stars,
                review=review
            )

            return JsonResponse({'message': 'user successfully created', 'review_id': rating.id}, status=201)
        else:
            return JsonResponse({'error': "only Post method is allowed"}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

def getRating(request):
    try:
        if request.method == "GET":
            # Select related hotel and user and return specific fields
            ratings = (
                Rating.objects
                .select_related('user', 'hotel')
                .values('id', 'stars', 'review', 'user__username', 'hotel__name', 'hotel__address')
            )
            return JsonResponse(list(ratings), safe=False, status=200)
        else:
            return JsonResponse({'message': 'Only GET method is allowed'}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
