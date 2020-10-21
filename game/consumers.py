from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection
import asyncio
import json

from .game_sessions import GameSessions
from .exceptions import MoveUnableException


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.player_id = self.scope['url_route']['kwargs']['player_id']
        
        try:
            GameSessions.get_by_id(self.session_id)
        except:
            raise DenyConnection('invalid session id')
        
        await self.channel_layer.group_add(
            self.session_id.__str__(),
            self.channel_name
        )

        await self.accept()
        await self.send_game_data('')

    async def send_game_data(self, event):
        game_session = GameSessions.get_by_id(self.session_id)

        data = {
            'game_field': game_session.game_field,
            'x_win_count': game_session.x_win_count,
            'o_win_count': game_session.o_win_count,
            'draw_count': game_session.draw_count,
            'restart_votes': game_session.restart_votes
        }
        await self.send(text_data=json.dumps(data))

    async def receive(self, text_data):
        try:
            received_data = json.loads(text_data)
        except Exception as e:
            print(type(e), e, text_data)
            return

        game_session = GameSessions.get_by_id(self.session_id)

        try:
            if received_data['command'] == 'move':
                game_session.move(int(self.player_id), received_data['x'], received_data['y'])
            elif received_data['command'] == 'restart':
                game_session.restart(self.player_id)
        except MoveUnableException:
            return
        except Exception as e:
            print(type(e), e, received_data)
            return

        await self.channel_layer.group_send(
            self.session_id.__str__(),
            {
                'type': 'send_game_data',
            }
        )

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.session_id.__str__(),
            self.channel_name
        )
