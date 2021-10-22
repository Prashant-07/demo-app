from django.conf import settings
from user.models import User,AccountStatus
import jwt

class JWTAuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authToken = request.META['HTTP_AUTHORIZATION']
            if authToken:
                authToken = str.replace(str(authToken), 'Bearer ', '')
                secret    = settings.SECRET_KEY
                try:
                    userData = jwt.decode(authToken, secret, algorithms=["HS256"])
                    user = User.objects.get(email=userData.get('email'))
                    if user.accountStatus == AccountStatus.ACTIVE and user.token == authToken:
                        request.user = user
                except:
                    pass
                response = self.get_response(request)
            else:
                response = self.get_response(request)
        else:
            response = self.get_response(request)
        return response
            
        

