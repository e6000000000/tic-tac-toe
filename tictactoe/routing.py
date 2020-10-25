from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from game.routing import websockets

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        websockets
    )
})