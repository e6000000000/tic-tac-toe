from django.urls import path
from . import views


urlpatterns = [
    path('<int:session_id>/<int:player_id>', views.game, name='game'),
    path('ai/<str:play_side>', views.game_with_ai, name='ai_game'),
    path('create/<str:play_side>', views.game_create, name='game_create'),
    path('', views.lobby, name='lobby'),
    path('statistic', views.statistic, name='statistic'),
]