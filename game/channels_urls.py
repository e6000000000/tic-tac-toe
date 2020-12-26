from django.urls import path

from .consumers import GameConsumer, AiGameConsumer, SearchConsumer


urlpatterns = [
    path("game/<int:session_id>/<int:player_id>", GameConsumer.as_asgi(), name="game_websocket"),
    path("aigame/<str:player_side>", AiGameConsumer.as_asgi(), name="aigame_websocket"),
    path("search/<str:player_side>", SearchConsumer.as_asgi(), name="search_websocket"),
]