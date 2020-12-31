from random import randrange
from threading import Thread
from time import sleep

from .game_field import TicTacToeField
from .exceptions import IdException
from .enums import GameStatus


class GameSession():
    """tic tac toe game session. 
    contains game field and info about win count

    Examples
    --------
    >>> game_session = GameSession()
    >>> player1_id = game_session.X_id
    >>> player2_id = game_session.O_id
    >>> game_session.game_status
    GameStatus.IN_PROGRESS
    >>> game_session.move(player1_id, 0, 0)
    >>> game_session.game_field
    [
        ['X', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    >>> game_session.move(player2_id, 1, 0)
    >>> game_session.game_field
    [
        ['X', 'O', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    >>> game_session.x_win_count
    0
    >>> game_session.move(player1_id, 1, 1)
    >>> game_session.move(player2_id, 2, 0)
    >>> game_session.move(player1_id, 2, 2)
    >>> game_session.game_field
    [
        ['X', 'O', 'O'],
        [' ', 'X', ' '],
        [' ', ' ', 'X']
    ]
    >>> game_session.game_status
    GameStatus.X_WIN
    >>> game_session.x_win_count
    1
    >>> game_session.restart()
    >>> game_session.game_field
    [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    >>> game_session.move(0, 0, 0) #invalid player id
    IdException: can't find player id=0
    >>> game_session.move(player_1, 12, 15) #invalid (x, y) or another kind of unable move
    MoveUnableException: ...

    """
    __sessions = {}
    next_id = 0

    def __init__(self):
        self.__player_quantity = 2
        self.__not_active_cooldown = 10*60
        self.__activity_timer = self.__not_active_cooldown

        self.__field = TicTacToeField()

        self.__X_id = randrange(10000, 50000)
        self.__O_id = randrange(50000, 99999)
        self.__restart_votes = []

        self.next_id += 1
        self.id = self.next_id
        self.x_win_count = 0
        self.o_win_count = 0
        self.draw_count = 0

        self.__sessions[self.id] = self
        self.__thread = Thread(target=self.__remove_if_not_active)
        self.__thread.start()

    def __remove_if_not_active(self):
        while 1:
            self.__activity_timer -= 1
            if self.__activity_timer <= 0:
                self.delete()
                break
            else:
                sleep(1)

    def __restart_activity_timer(self):
        self.__activity_timer = self.__not_active_cooldown

    def delete(self) -> None:
        """remove GameSession from __sessions
        """
        try:
            GameSession.__sessions.pop(self.id)
        except:
            raise IdException(f'can\'t find session id={self.id}')

    @staticmethod
    def get_by_id(session_id:int):
        """return a GameSession by id
        """
        try:
            return GameSession.__sessions[session_id]
        except:
            raise IdException(f'can\'t find session id={session_id}')

    @property
    def X_id(self) -> int:
        return self.__X_id

    @property
    def O_id(self) -> int:
        return self.__O_id

    @property
    def move_count(self) -> int:
        return self.__field.move_count

    @property
    def restart_votes(self) -> int:
        return self.__restart_votes.__len__()

    def restart(self, player_id):
        """vote to clear game field, 
        if all players vote field will be cleared
        """
        if player_id not in self.__restart_votes:
            self.__restart_votes.append(player_id)

        if self.__restart_votes.__len__() >= self.__player_quantity:
            self.__field = TicTacToeField()
            self.__restart_votes.clear()

        self.__restart_activity_timer()

    def move(self, player_id:int, x:int, y:int):
        """try move like X or O (depends on player_id) to
        (x, y), which should be in 0..2
        """
        if player_id == self.__X_id:
            self.__field.move_X(x, y)
        elif player_id == self.__O_id:
            self.__field.move_O(x, y)
        else:
            raise IdException(f'can\'t find player id={player_id}')

        self.__update_stats()
        self.__restart_activity_timer()

        

    @property
    def game_status(self) -> GameStatus:
        return self.__field.status

    @property
    def game_field(self):
        """field looks like:\n
        [\n
         ['X', 'O', ' '],\n
         [' ', 'X', ' '],\n
         ['O', ' ', 'X'],\n
        ]\n
        it's list of lists of strings\n
        """
        return self.__field.get()


    def __update_stats(self):
        game_status = self.__field.status
        if game_status == GameStatus.X_WIN:
            self.x_win_count += 1
        if game_status == GameStatus.O_WIN:
            self.o_win_count += 1
        if game_status == GameStatus.DRAW:
            self.draw_count += 1

