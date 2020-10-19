from channels.routing import ProtocolTypeRouter, URLRouter
from game.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})