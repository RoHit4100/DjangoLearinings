import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate

class BasicAuthMiddleware:
    def __init__(self, getResponse) -> None:
        self.getResponse = getResponse
        
    def __call__(self, request, *args, **kwargs):
        try:
        # get the authentication header
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            # check if auth header is provided or not
            if not auth_header or not auth_header.startswith('Basic'):
                return HttpResponse("Authentication header is not provided", status=400)
            
            
            # decode and authenticate
            encoded_credentials = auth_header.split(' ')[1]
            # decode 
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8').split(':')
            username = decoded_credentials[0]
            password = decoded_credentials[1]
            
            # authenticate the user
            user = authenticate(username=username, password=password) # if user not found none will returned
            if not user:
                return HttpResponse('Invalid credentials', status=401)
            
            request.username = username
            # get the response
            response = self.getResponse(request)
            return response
        except Exception as e:
            return HttpResponse(str(e), status=400)