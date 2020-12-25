from collections import namedtuple
from queue import Queue
import asyncio

from .game_sessions import GameSessions
from .Statistic import Statistic


SearchResult = namedtuple('search_result', ('session_id', 'player_id'))


class SearchingPlayer:
    def __init__(self, play_side: str):
        if play_side.lower() in ('x', 'o'):
            self.play_side = play_side.lower()
            self.game_session_id = None
        else:
            raise ValueError(f'play_side should be in ("X", "O"), not {play_side}')
        

    async def await_for_find(self):
        while 1:
            if self.game_session_id is None:
                await asyncio.sleep(1)
            else:
                return self.make_result()

    def finded(self, other_player):
        if type(other_player) is not SearchingPlayer:
            raise TypeError(f'type of other_player should be SearchingPlayer, not {type(other_player)}')

        self.game_session_id = GameSessions.new()
        other_player.game_session_id = self.game_session_id
        return self.make_result()

    def make_result(self):
        game_session = GameSessions.get_by_id(self.game_session_id) 
        player_id = game_session.X_id if self.play_side == 'x' else game_session.O_id
        return SearchResult(self.game_session_id, player_id)



class GameSearch:
    """class that helps with a game search. 
    player_side should be str, "X" or "O"
    """
    count = 0
    X_searchers = []
    O_searchers = []

    def __init__(self, player_side: str):
        if player_side.lower() not in ('x', 'o'):
            raise ValueError(f'player_side should be "x" or "o", not "{player_side}"')
        self.player_side = player_side
        self.player = SearchingPlayer(self.player_side)
        
        if self.player_side.lower() == 'x':
            self.player_side_searchers = self.X_searchers
            self.other_side_searchers = self.O_searchers
        elif self.player_side.lower() == 'o':
            self.player_side_searchers = self.O_searchers
            self.other_side_searchers = self.X_searchers

    async def search(self) -> SearchResult:
        """search for a game.

        method will be in progress while searching
        and return SearchResult at the end.
        """

        if self.player_side.lower() == 'x':
            Statistic.players_Xsearch += 1
        elif self.player_side.lower() == 'o':
            Statistic.players_Osearch += 1

        if not self.other_side_searchers.__len__() <= 0:
            other_player = self.other_side_searchers.pop(0)
            other_player.finded(self.player)
            return self.player.make_result()

        self.player_side_searchers.append(self.player)
        return await self.player.await_for_find()

    def cancel_search(self):
        """cancel started search
        """
        if self.player_side.lower() == 'x':
            Statistic.players_Xsearch -= 1
        elif self.player_side.lower() == 'o':
            Statistic.players_Osearch -= 1

        if self.player in self.player_side_searchers:
            del self.player_side_searchers[self.player_side_searchers.index(self.player)]