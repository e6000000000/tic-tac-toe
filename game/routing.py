from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import GameConsumer, AiGameConsumer

websockets = URLRouter([
    path("ws/<int:session_id>/<int:player_id>", GameConsumer, name="game_websocket"),
    path("aiws/<str:player_side>", AiGameConsumer, name="aigame_websocket"),
])
