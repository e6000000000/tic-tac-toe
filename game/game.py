from enum import Enum

import unittest


class GameFieldSizeException(Exception):
    def __init__(self, text:str):
        self.txt = text

class CellAlreadySetedException(Exception):
    def __init__(self, x:int, y:int):
        self.txt = f'x={x} y={y}'

class MoveLimitReachedException(Exception):
    def __init__(self, move_number, limit):
        self.txt = f'move_number={move_number} limit={limit}'

class GameAlreadyEndedException(Exception):
    pass


class GameStatus(Enum):
    IN_PROGRESS = 1
    X_WIN = 2
    O_WIN = 3
    DRAW = 4

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

    def move(self, x, y):
        if self.__move_count >= 9:
            raise MoveLimitReachedException(self.__move_count + 1, self.__field_size ** 2)

        if self.get_status() != GameStatus.IN_PROGRESS:
            raise GameAlreadyEndedException()

        if self.__move_count % 2:
            self.__set_O(x, y)
        else:
            self.__set_X(x, y)

        self.__move_count += 1
        

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
            raise GameFieldSizeException(f'x={x} not in range {self.__field_size}')
        if y not in range(self.__field_size):
            raise GameFieldSizeException(f'y={y} not in range {self.__field_size}')
        if self.__game_field[x][y] != self.__empty_cell_symbol:
            raise CellAlreadySetedException(x, y)

        self.__game_field[x][y] = symbol

    def __set_X(self, x, y):
        return self.__set_symbol(x, y, 'X')

    def __set_O(self, x, y):
        return self.__set_symbol(x, y, 'O')









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
        tictactoe.move(1, 1)

        self.assertEqual(tictactoe.get_game_field(), [
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_second_move(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move(1, 1)
        tictactoe.move(0, 0)

        self.assertEqual(tictactoe.get_game_field(), [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_X_win(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move(1, 1)
        tictactoe.move(0, 0)
        tictactoe.move(0, 1)
        tictactoe.move(1, 0)
        tictactoe.move(2, 1)

        self.assertEqual(tictactoe.get_status(), GameStatus.X_WIN)

    def test_O_win(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move(2, 2)
        tictactoe.move(1, 1)
        tictactoe.move(0, 0)
        tictactoe.move(0, 1)
        tictactoe.move(1, 0)
        tictactoe.move(2, 1)

        self.assertEqual(tictactoe.get_status(), GameStatus.O_WIN)

    def test_in_progress(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move(2, 2)
        tictactoe.move(1, 1)
        tictactoe.move(0, 0)
        tictactoe.move(0, 1)
        tictactoe.move(1, 0)

        self.assertEqual(tictactoe.get_status(), GameStatus.IN_PROGRESS)

    def test_draw(self):
        tictactoe = TicTacToeBatch()
        tictactoe.move(0, 0)
        tictactoe.move(0, 1)
        tictactoe.move(0, 2)
        tictactoe.move(2, 0)
        tictactoe.move(2, 1)
        tictactoe.move(2, 2)
        tictactoe.move(1, 0)
        tictactoe.move(1, 1)
        tictactoe.move(1, 2)

        self.assertEqual(tictactoe.get_status(), GameStatus.DRAW)


if __name__ == '__main__':
    unittest.main()
