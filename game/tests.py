from django.test import TestCase
import unittest

from .game_field import TicTacToeField
from .enums import GameStatus


class TestUM(unittest.TestCase):
    def setUp(self):
        self.field = TicTacToeField()

    def tearDown(self):
        pass

    def test_empty_field_generation(self):
        self.assertEqual(self.field.get(), [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ])

    def test_first_move(self):
        self.field.move_X(1, 1)

        self.assertEqual(self.field.get(), [
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_second_move(self):
        self.field.move_X(1, 1)
        self.field.move_O(0, 0)

        self.assertEqual(self.field.get(), [
            ['O', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ])

    def test_X_win(self):
        self.field.move_X(1, 1)
        self.field.move_O(0, 0)
        self.field.move_X(0, 1)
        self.field.move_O(1, 0)
        self.field.move_X(2, 1)

        self.assertEqual(self.field.status, GameStatus.X_WIN)

    def test_O_win(self):
        self.field.move_X(2, 2)
        self.field.move_O(1, 1)
        self.field.move_X(0, 0)
        self.field.move_O(0, 1)
        self.field.move_X(1, 0)
        self.field.move_O(2, 1)

        self.assertEqual(self.field.status, GameStatus.O_WIN)

    def test_in_progress(self):
        self.field.move_X(2, 2)
        self.field.move_O(1, 1)
        self.field.move_X(0, 0)
        self.field.move_O(0, 1)
        self.field.move_X(1, 0)

        self.assertEqual(self.field.status, GameStatus.IN_PROGRESS)

    def test_draw(self):
        self.field.move_X(0, 0)
        self.field.move_O(0, 1)
        self.field.move_X(0, 2)
        self.field.move_O(2, 0)
        self.field.move_X(2, 1)
        self.field.move_O(2, 2)
        self.field.move_X(1, 0)
        self.field.move_O(1, 1)
        self.field.move_X(1, 2)

        self.assertEqual(self.field.status, GameStatus.DRAW)


def main():
    unittest.main()