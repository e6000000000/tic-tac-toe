import unittest

from .ai import TicTacToeAi
from .enums import GameStatus


class TestUM(unittest.TestCase):
    def setUp(self):
        self.ai = TicTacToeAi()

    def tearDown(self):
        pass

    def test_one_step_win(self):
        self.assertEqual(self.ai.best_move([
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            [' ', ' ', ' '],
        ]), (GameStatus.X_WIN, 2, 2))

    def test_one_step_draw_or_win(self):
        self.assertEqual(self.ai.best_move([
            ['X', 'O', 'O'],
            ['X', 'X', 'O'],
            [' ', 'X', ' '],
        ]), (GameStatus.O_WIN, 2, 2))

    def test_two_step_win(self):
        self.assertIn(self.ai.best_move([
            [' ', 'O', 'X'],
            [' ', 'X', ' '],
            ['O', ' ', ' '],
        ]), ((GameStatus.X_WIN, 2, 1), (GameStatus.X_WIN, 2, 2)))

    def test_draw_or_lose(self):
        self.assertEqual(self.ai.best_move([
            [' ', 'O', 'X'],
            ['O', 'X', ' '],
            ['O', 'X', ' '],
        ]), (GameStatus.DRAW, 0, 0))

    def test_only_one(self):
        self.assertEqual(self.ai.best_move([
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', ' '],
        ]), (GameStatus.DRAW, 2, 2))

    def test_first(self): #i realy don't know what move is the best now
        self.assertEqual(self.ai.best_move([
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
        ]), (GameStatus.DRAW, 0, 0))


def main():
    unittest.main()