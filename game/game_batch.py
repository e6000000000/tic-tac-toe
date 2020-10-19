import unittest

from .exceptions import MoveUnableException
from .enums import GameStatus


class TicTacToeBatch():
    __field_size = 3
    __empty_cell_symbol = ' '
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

    def __init__(self):
        self.__game_field = [[self.__empty_cell_symbol for x in range(self.__field_size)] for x in range(self.__field_size)]
        self.__move_count = 0


    def get_game_field(self) -> list:
        """game field looks like:\n
        [\n
         ['X', 'O', ' '],\n
         [' ', 'X', ' '],\n
         ['O', ' ', 'X'],\n
        ]\n
        it's list of lists of strings\n
        """

        return self.__game_field

    def get_status(self):
        if self.__is_X_win():
            return GameStatus.X_WIN
        elif self.__is_O_win():
            return GameStatus.O_WIN
        elif self.__is_draw():
            return GameStatus.DRAW
        else:
            return GameStatus.IN_PROGRESS

    def __move(self, symbol, x, y):
        if self.get_status() != GameStatus.IN_PROGRESS:
            raise MoveUnableException('game already ended')

        self.__set_symbol(x, y, symbol)

        self.__move_count += 1

    def move_X(self, x, y):
        """"""
        if self.__move_count % 2:
            raise MoveUnableException('now is O move time')
        return self.__move('X', x, y)

    def move_O(self, x, y):
        """"""
        if not self.__move_count % 2:
            raise MoveUnableException('now is X move time')
        return self.__move('O', x, y)
        

    def __is_symbol_win(self, symbol):
        for position in self.__win_positions:
            for x, y in position:
                if self.__game_field[x][y] != symbol:
                    break
            else:
                return True
        return False

    def __is_X_win(self):
        return self.__is_symbol_win('X')

    def __is_O_win(self):
        return self.__is_symbol_win('O')

    def __is_draw(self):
        return not self.__is_X_win() and not self.__is_O_win() and self.__move_count == 9

    def __set_symbol(self, x, y, symbol:str) -> None:
        if x not in range(self.__field_size):
            raise MoveUnableException(f'x={x} not in range {self.__field_size}')
        if y not in range(self.__field_size):
            raise MoveUnableException(f'y={y} not in range {self.__field_size}')
        if self.__game_field[x][y] != self.__empty_cell_symbol:
            raise MoveUnableException('cell already seted')

        self.__game_field[x][y] = symbol









#tests
class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_field_generation(self):
        tictactoe = TicTacToeBatch()

        self.assertEqual(tictactoe.get_game_field(), [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ])

    def test_first_move(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(1, 1)

        self.assertEqual(tictactoe.get_game_field(), [
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_second_move(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(1, 1)
        tictactoe.move_O(0, 0)

        self.assertEqual(tictactoe.get_game_field(), [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_X_win(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(1, 1)
        tictactoe.move_O(0, 0)
        tictactoe.move_X(0, 1)
        tictactoe.move_O(1, 0)
        tictactoe.move_X(2, 1)

        self.assertEqual(tictactoe.get_status(), GameStatus.X_WIN)

    def test_O_win(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(2, 2)
        tictactoe.move_O(1, 1)
        tictactoe.move_X(0, 0)
        tictactoe.move_O(0, 1)
        tictactoe.move_X(1, 0)
        tictactoe.move_O(2, 1)

        self.assertEqual(tictactoe.get_status(), GameStatus.O_WIN)

    def test_in_progress(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(2, 2)
        tictactoe.move_O(1, 1)
        tictactoe.move_X(0, 0)
        tictactoe.move_O(0, 1)
        tictactoe.move_X(1, 0)

        self.assertEqual(tictactoe.get_status(), GameStatus.IN_PROGRESS)

    def test_draw(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move_X(0, 0)
        tictactoe.move_O(0, 1)
        tictactoe.move_X(0, 2)
        tictactoe.move_O(2, 0)
        tictactoe.move_X(2, 1)
        tictactoe.move_O(2, 2)
        tictactoe.move_X(1, 0)
        tictactoe.move_O(1, 1)
        tictactoe.move_X(1, 2)

        self.assertEqual(tictactoe.get_status(), GameStatus.DRAW)


if __name__ == '__main__':
    unittest.main()
