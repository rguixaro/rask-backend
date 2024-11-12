from django.urls import path
from .views import links,link,link_exists,link_create,authenticate


urlpatterns = [
    path('links', links),
    path('link/<slug:slug>', link),
    path('link-exists/<slug:slug>', link_exists),
    path('link-create', link_create),
    path('auth', authenticate),
]
