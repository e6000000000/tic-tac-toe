import copy

from .exceptions import MoveUnableException
from .enums import GameStatus


class TicTacToeField():
    """core game class. 
    field 3x3 to draw X and O and get information who wins

    field should looks like:
    [
        ['X', 'O', ' '],
        [' ', 'X', ' '],
        [' ', ' ', ' ']
    ]
    list of lists of strs
    """
    field_size = 3
    empty_cell_symbol = ' '
    __win_positions = (
        ((0, 0),(0, 1),(0, 2)),
        ((1, 0),(1, 1),(1, 2)),
        ((2, 0),(2, 1),(2, 2)),
        ((0, 0),(1, 0),(2, 0)),
        ((0, 1),(1, 1),(2, 1)),
        ((0, 2),(1, 2),(2, 2)),
        ((0, 0),(1, 1),(2, 2)),
        ((0, 2),(1, 1),(2, 0)),
    )

    def __init__(self, field:list=None):
        if field is None:
            self.__field = [[self.empty_cell_symbol for x in range(self.field_size)] for y in range(self.field_size)]
        else:
            if self.__is_field_valid(field):
                self.__field = copy.deepcopy(field)
            else:
                raise ValueError('invalid field')
        
        self.move_count = 0
        for row in self.__field:
            for symbol in row:
                if symbol != self.empty_cell_symbol:
                    self.move_count += 1

    def __is_field_valid(self, field:list):
        try:
            for y in range(self.field_size):
                for x in range(self.field_size):
                    if field[y][x].lower() not in (self.empty_cell_symbol, 'x', 'o'):
                        raise Exception()
        except:
            return False
        return True

    def get(self) -> list:
        """field looks like:\n
        [\n
         ['X', 'O', ' '],\n
         [' ', 'X', ' '],\n
         ['O', ' ', 'X'],\n
        ]\n
        it's list of lists of strings\n
        """

        return self.__field

    @property
    def status(self) -> GameStatus:
        if self.__is_X_win():
            return GameStatus.X_WIN
        elif self.__is_O_win():
            return GameStatus.O_WIN
        elif self.__is_draw():
            return GameStatus.DRAW
        else:
            return GameStatus.IN_PROGRESS

    def __move(self, symbol:str, x:int, y:int):
        if self.status != GameStatus.IN_PROGRESS:
            raise MoveUnableException('game already ended')

        self.__set_symbol(x, y, symbol)

        self.move_count += 1

    def move_X(self, x:int, y:int):
        """try set X to (x, y), which should be in 0..2"""
        if self.move_count % 2:
            raise MoveUnableException('now is O move time')
        return self.__move('X', x, y)

    def move_O(self, x:int, y:int):
        """try set O to (x, y), which should be in 0..2"""
        if not self.move_count % 2:
            raise MoveUnableException('now is X move time')
        return self.__move('O', x, y)
        

    def __is_win(self, symbol:str):
        for position in self.__win_positions:
            for x, y in position:
                if self.__field[y][x].lower() != symbol.lower():
                    break
            else:
                return True
        return False

    def __is_X_win(self):
        return self.__is_win('X')

    def __is_O_win(self):
        return self.__is_win('O')

    def __is_draw(self):
        return not self.__is_X_win() and not self.__is_O_win() and self.move_count == 9

    def __set_symbol(self, x:int, y:int, symbol:str) -> None:
        if x not in range(self.field_size):
            raise MoveUnableException(f'x={x} not in range {self.field_size}')
        if y not in range(self.field_size):
            raise MoveUnableException(f'y={y} not in range {self.field_size}')
        if self.__field[y][x] != self.empty_cell_symbol:
            raise MoveUnableException('cell already seted')

        self.__field[y][x] = symbol
