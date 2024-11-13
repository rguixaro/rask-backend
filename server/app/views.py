from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Link, Session
from .serializers import LinkSerializer
from .link import generate_link
from .sessions import create_new_session
from .tokens import generate_access_cookie,store_cookies,decode_token


@api_view(['GET'])
def links_list(request):
    if request.method == 'GET':
        if not 'rask_session' in request.COOKIES:
            return Response(status=401, data={'error': True, 'message': 'UNAUTHORIZED'})
        else:
            access_token = request.COOKIES['rask_session']
            token = decode_token(access_token)
            if not 'success' in token:
                return Response(status=401, data={'error': True, 'message': 'UNAUTHORIZED'})
            else:
                sessionId = token['value']['session_id']
                links = Link.objects.filter(created_by = sessionId).defer('created_by')
                serializer = LinkSerializer(links, many=True, fields=['url', 'slug', 'visits' ,'created_at'])
                return Response(status=200, data={'error': False, 'list': serializer.data})
    
@api_view(['GET'])
def link_check(request, slug: str):
    if request.method == 'GET':
        try:
            link = Link.objects.get(slug = slug)
            link.visits += 1
            link.save()
            return Response(status=200, data={'error': False, 'url': link.url})
        except Link.DoesNotExist:
            return Response(status=200, data={'error': True, 'message': 'LINK_NOT_FOUND'})

@api_view(['GET'])
def link_exists(request, slug: str):
    if request.method == 'GET':
        link = Link.objects.filter(slug = slug)
        if link:
            return Response(status=200, data={'error': True, 'message': 'LINK_EXISTS'})
        else:
            return Response(status=200, data={'error': False})
    
@api_view(['POST'])
def link_create(request):
    if request.method == 'POST':
        if not 'rask_session' in request.COOKIES:
            return Response(status=401, data={'error': True, 'message': 'UNAUTHORIZED'})
        else:
            access_token = request.COOKIES['rask_session']
            token = decode_token(access_token)
            sessionId = token['value']['session_id']
            session = Session.objects.get(id=sessionId)
            if session.urls_created >= 10:
                return Response(status=403, data={'error': True, 'message': 'LINK_LIMIT_REACHED'})
            if 'url' not in request.data:
                return Response(status=400, data={'error': True, 'message': 'LINK_URL_REQUIRED'})
            elif 'slug' not in request.data:
                request.data['slug'] = generate_link()
            request.data['created_by'] = sessionId
            serializer = LinkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                session.urls_created += 1
                session.save()
                return Response(status=201, data={'error': False})
            return Response(status=400 ,data={'error': True, 'message': 'INVALID_DATA'})
    
@api_view(['POST'])
def authenticate(request):
    if request.method == 'POST':
        if not 'rask_uuid' in request.COOKIES: 
            return create_new_session()
        else:
            refresh_token = request.COOKIES['rask_uuid']
            token = decode_token(refresh_token)
            if not 'success' in token:
                return create_new_session()
            else: 
                if not 'rask_session' in request.COOKIES:
                    sessionId = token['value']['session_id']
                    new_access_token = generate_access_cookie(sessionId)
                    response = store_cookies(refresh_token, new_access_token)
                    return response
                else: 
                    access_token = request.COOKIES['rask_session']
                    token = decode_token(access_token)
                    if not 'success' in token:
                        sessionId = token['value']['session_id']
                        new_access_token = generate_access_cookie(sessionId)
                        response = store_cookies(refresh_token, new_access_token)
                        return response
                    else:
                        return Response(status=200, data={'error': False})