import jwt,datetime
from django.conf import settings

def getRequestIp(request):
    ipHeader = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = ''
    if ipHeader:
        ip = ipHeader.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generateToken(request,params={}):
    ip = getRequestIp(request)
    secret = settings.SECRET_KEY
    params['exp'] = datetime.datetime.now() + datetime.timedelta(minutes = 15)
    token = jwt.encode(params, secret , algorithm="HS256")
    return token
    