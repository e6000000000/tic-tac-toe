from django.test import TestCase
import unittest

from .game_field import TicTacToeField
from .enums import GameStatus


class TestUM(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty_field_generation(self):
        field = TicTacToeField()

        self.assertEqual(field.get(), [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ])

    def test_first_move(self):
        field = TicTacToeField()
        field.move_X(1, 1)

        self.assertEqual(field.get(), [
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_second_move(self):
        field = TicTacToeField()
        field.move_X(1, 1)
        field.move_O(0, 0)

        self.assertEqual(field.get(), [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_X_win(self):
        field = TicTacToeField()
        field.move_X(1, 1)
        field.move_O(0, 0)
        field.move_X(0, 1)
        field.move_O(1, 0)
        field.move_X(2, 1)

        self.assertEqual(field.status, GameStatus.X_WIN)

    def test_O_win(self):
        field = TicTacToeField()
        field.move_X(2, 2)
        field.move_O(1, 1)
        field.move_X(0, 0)
        field.move_O(0, 1)
        field.move_X(1, 0)
        field.move_O(2, 1)

        self.assertEqual(field.status, GameStatus.O_WIN)

    def test_in_progress(self):
        field = TicTacToeField()
        field.move_X(2, 2)
        field.move_O(1, 1)
        field.move_X(0, 0)
        field.move_O(0, 1)
        field.move_X(1, 0)

        self.assertEqual(field.status, GameStatus.IN_PROGRESS)

    def test_draw(self):
        field = TicTacToeField()
        field.move_X(0, 0)
        field.move_O(0, 1)
        field.move_X(0, 2)
        field.move_O(2, 0)
        field.move_X(2, 1)
        field.move_O(2, 2)
        field.move_X(1, 0)
        field.move_O(1, 1)
        field.move_X(1, 2)

        self.assertEqual(field.status, GameStatus.DRAW)


if __name__ == '__main__':
    unittest.main()