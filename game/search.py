from collections import namedtuple
from queue import Queue
import asyncio

from .game_sessions import GameSessions


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
                await asyncio.sleep(0.666)
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
    """
    X_searchers = Queue()
    O_searchers = Queue()

    @staticmethod
    async def search(player_side: str) -> SearchResult:
        """search for a game.
        player_side should be str, "X" or "O"

        method will be in progress while searching
        and return SearchResult at the end.
        """
        player = SearchingPlayer(player_side)
        
        if player_side.lower() == 'x':
            player_side_searchers = GameSearch.X_searchers
            other_side_searchers = GameSearch.O_searchers
        elif player_side.lower() == 'o':
            player_side_searchers = GameSearch.O_searchers
            other_side_searchers = GameSearch.X_searchers

        if not other_side_searchers.empty():
            other_player = other_side_searchers.get()
            other_player.finded(player)
            return player.make_result()

        player_side_searchers.put(player)
        return await player.await_for_find()