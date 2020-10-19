from random import randrange

from . import game_batch
from .exceptions import IdException
from .enums import GameStatus


class GameSession():
    def __init__(self):
        self.__batch = game_batch.TicTacToeBatch()

        self.__player1_id = randrange(10000, 50000)
        self.__player2_id = randrange(50000, 99999)

        self.x_win_count = 0
        self.o_win_count = 0
        self.draw_count = 0

    @property
    def player1_id(self):
        return self.__player1_id

    @property
    def player2_id(self):
        return self.__player2_id

    def restart(self):
        self.__batch = game_batch.TicTacToeBatch()

    def move(self, player_id, x, y):
        if player_id == self.__player1_id:
            self.__batch.move_X(x, y)
        elif player_id == self.__player2_id:
            self.__batch.move_O(x, y)
        else:
            raise IdException(f'can\'t find player id={player_id}')

        self.__update_stats()

        

    @property
    def game_status(self):
        return self.__batch.get_status()

    @property
    def game_field(self):
        return self.__batch.get_game_field()


    def __update_stats(self):
        game_status = self.__batch.get_status()
        if game_status == GameStatus.X_WIN:
            self.x_win_count += 1
        if game_status == GameStatus.O_WIN:
            self.o_win_count += 1
        if game_status == GameStatus.DRAW:
            self.draw_count += 1

