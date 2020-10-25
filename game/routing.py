from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import GameConsumer, AiGameConsumer, SearchConsumer

websockets = URLRouter([
    path("ws/<int:session_id>/<int:player_id>", GameConsumer, name="game_websocket"),
    path("aiws/<str:player_side>", AiGameConsumer, name="aigame_websocket"),
    path("searchws/<str:player_side>", SearchConsumer, name="search_websocket"),
])
