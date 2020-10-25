from django.urls import path

from .consumers import GameConsumer, AiGameConsumer, SearchConsumer


urlpatterns = [
    path("game/<int:session_id>/<int:player_id>", GameConsumer, name="game_websocket"),
    path("aigame/<str:player_side>", AiGameConsumer, name="aigame_websocket"),
    path("search/<str:player_side>", SearchConsumer, name="search_websocket"),
]