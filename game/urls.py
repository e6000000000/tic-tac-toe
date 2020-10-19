from django.urls import path
from . import views


urlpatterns = [
    path('<int:session_id>/<int:player_id>', views.game, name='game'),
    path('', views.game_create, name='game_create'),
]