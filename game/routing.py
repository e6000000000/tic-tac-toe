from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .channels_urls import urlpatterns

websockets = URLRouter(urlpatterns)
