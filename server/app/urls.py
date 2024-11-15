from django.urls import path
from .views import links_list,link_check,link_exists,link_create,authenticate


urlpatterns = [
    path('links-list', links_list),
    path('link-check/<slug:slug>', link_check),
    path('link-exists/<slug:slug>', link_exists),
    path('link-create', link_create),
    path('auth', authenticate),
]
