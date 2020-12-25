from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection, StopConsumer
from django.urls import reverse
import json
import asyncio

from .game_sessions import GameSessions
from .game_session import GameSession
from . enums import GameStatus
from .exceptions import MoveUnableException
from .ai import TicTacToeAi
from .search import GameSearch
from .Statistic import Statistic


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
        await self.send_game_data()
        Statistic.players_now += 1

    async def send_game_data(self, event=''):
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

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_id.__str__(),
            self.channel_name
        )
        Statistic.players_now -= 1


class AiGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_session = GameSession()
        player_side = self.scope['url_route']['kwargs']['player_side']
        self.player_id = self.game_session.O_id if player_side.lower() == 'o' else self.game_session.X_id
        
        await self.accept()
        await self.ai_move_if_need()
        await self.send_game_data()

    async def send_game_data(self, event=''):
        data = {
            'game_field': self.game_session.game_field,
            'x_win_count': self.game_session.x_win_count,
            'o_win_count': self.game_session.o_win_count,
            'draw_count': self.game_session.draw_count,
            'restart_votes': self.game_session.restart_votes
        }
        await self.send(text_data=json.dumps(data))

    async def ai_move_if_need(self):
        if self.player_id == self.game_session.X_id and self.game_session.move_count % 2 or\
           self.player_id == self.game_session.O_id and not self.game_session.move_count % 2:
            if self.game_session.game_status == GameStatus.IN_PROGRESS:
                TicTacToeAi.move(self.game_session)

    async def receive(self, text_data):
        try:
            received_data = json.loads(text_data)
        except Exception as e:
            print(type(e), e, text_data)
            return

        try:
            if received_data['command'] == 'move':
                self.game_session.move(int(self.player_id), received_data['x'], received_data['y'])
            elif received_data['command'] == 'restart':
                self.game_session.restart(self.game_session.X_id)
                self.game_session.restart(self.game_session.O_id)
        except MoveUnableException:
            return
        except Exception as e:
            print(type(e), e, received_data)
            return

        await self.ai_move_if_need()
        await self.send_game_data()

    async def disconnect(self, close_code):
        pass


class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.player_side = self.scope['url_route']['kwargs']['player_side']
        
        await self.accept()

        self.game_seearch = GameSearch(self.player_side)
        asyncio.run_coroutine_threadsafe(self.start_search(), asyncio.get_running_loop())

    async def start_search(self):
        result = await self.game_seearch.search()
        url = reverse('game', args=(result.session_id, result.player_id))
        await self.send(text_data=url)
        await self.close(1000)

    async def receive(self, text_data):
        pass

    async def disconnect(self, close_code):
        self.game_seearch.cancel_search()
