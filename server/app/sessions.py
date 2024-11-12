
import secrets
from .models import  Session
from .tokens import generate_cookies, store_cookies

def create_new_session():
    sessionId = secrets.token_urlsafe(32)
    Session.objects.create(id=sessionId)
    refresh_token,access_token = generate_cookies(sessionId)
    response = store_cookies(refresh_token, access_token)
    return response;