from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from .consumers import GameConsumer

websockets = URLRouter([
    path("ws/<int:session_id>/<int:player_id>", GameConsumer, name="game_websocket"),
])
