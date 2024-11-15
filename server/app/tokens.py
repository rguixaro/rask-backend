from django.http import HttpResponse
from dotenv import load_dotenv
import jwt
import os

from .utils import getHourlyExpirationTime, getYearlyExpirationTime

load_dotenv()
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

def generate_cookies(sessionId):
    refresh_token = jwt.encode({'session_id': sessionId, 'exp': getYearlyExpirationTime() }, ENCRYPTION_KEY, algorithm="HS256")
    access_token = generate_access_cookie(sessionId)
    return refresh_token,access_token

def generate_access_cookie(sessionId):
    access_token = jwt.encode({'session_id': sessionId, 'exp': getHourlyExpirationTime() }, ENCRYPTION_KEY, algorithm="HS256")
    return access_token

def store_cookies(refresh_token, access_token):
    response = HttpResponse(status=200)
    response.set_cookie(key= 'rask_uuid',
        value= refresh_token,
        max_age=60*60*24*365,
        secure=True,
        httponly=True,
        samesite='Strict    ',
        domain='rask.rguixaro.dev'

    )
    response.set_cookie(key= 'rask_session',
        value= access_token,
        max_age=60*60,
        secure=True,
        httponly=True,
        samesite='Strict',
        domain='rask.rguixaro.dev'
    )
    return response

def decode_token(token):
    try:
        value = jwt.decode(token, ENCRYPTION_KEY, algorithms=["HS256"])
        return {'success': True, 'value': value}
    except jwt.ExpiredSignatureError:        
        return {'success': False, 'error': 'TOKEN_EXPIRED'}