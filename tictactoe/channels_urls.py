from django.urls import path, include


urlpatterns = [
    path('', include('game.channels_urls')),
]