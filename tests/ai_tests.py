import unittest

from game.ai import TicTacToeAi
from game.enums import GameStatus


class TestUM(unittest.TestCase):
    def setUp(self):
        self.ai = TicTacToeAi()

    def tearDown(self):
        pass

    def test_one_step_win(self):
        self.assertEqual(self.ai.move_coordinates([
            ['X', 'O', ' '],
            [' ', 'X', 'O'],
            [' ', ' ', ' '],
        ]), (GameStatus.X_WIN, 2, 2))

    def test_one_step_draw_or_win(self):
        self.assertEqual(self.ai.move_coordinates([
            ['X', 'O', 'O'],
            ['X', 'X', 'O'],
            [' ', 'X', ' '],
        ]), (GameStatus.O_WIN, 2, 2))

    def test_two_step_win(self):
        self.assertIn(self.ai.move_coordinates([
            [' ', 'O', 'X'],
            [' ', 'X', ' '],
            ['O', ' ', ' '],
        ]), ((GameStatus.X_WIN, 2, 1), (GameStatus.X_WIN, 2, 2)))

    def test_draw_or_lose(self):
        self.assertEqual(self.ai.move_coordinates([
            [' ', 'O', 'X'],
            ['O', 'X', ' '],
            ['O', 'X', ' '],
        ]), (GameStatus.DRAW, 0, 0))

    def test_only_one(self):
        self.assertEqual(self.ai.move_coordinates([
            ['X', 'O', 'X'],
            ['X', 'O', 'O'],
            ['O', 'X', ' '],
        ]), (GameStatus.DRAW, 2, 2))

    def test_second_move(self): #i realy don't know what move is the best for now
        self.assertIn(self.ai.move_coordinates([
            [' ', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' '],
        ]), (
                (GameStatus.IN_PROGRESS, 0, 0),
                (GameStatus.IN_PROGRESS, 0, 1),
                (GameStatus.IN_PROGRESS, 0, 2),
                (GameStatus.IN_PROGRESS, 1, 0),
                (GameStatus.IN_PROGRESS, 1, 2),
                (GameStatus.IN_PROGRESS, 2, 0),
                (GameStatus.IN_PROGRESS, 2, 1),
                (GameStatus.IN_PROGRESS, 2, 2),
            ))

    def test_1(self):
        self.assertEqual(self.ai.move_coordinates([
            ['O', 'O', 'X'],
            ['O', 'X', ' '],
            [' ', ' ', 'X'],
        ]), (GameStatus.X_WIN, 2, 1))


def main():
    unittest.main()