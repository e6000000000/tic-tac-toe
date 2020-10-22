from collections import namedtuple
from random import randrange

from .game_field import TicTacToeField
from .game_session import GameSession
from .enums import GameStatus


Point = namedtuple('Point', ('status', 'x', 'y'))

class TicTacToeAi:
    __empty_cell_symbol = TicTacToeField.empty_cell_symbol
    __field_size = TicTacToeField.field_size


    @staticmethod
    def move(game_session: GameSession):
        point = TicTacToeAi.move_coordinates(game_session.game_field)
        game_session.move( game_session.O_id if game_session.move_count % 2 else game_session.X_id,
            point.x, point.y
        )

    @staticmethod
    def move_coordinates(field_:list) -> Point:
        """field_ should looks like:
        [
            ['X', 'O', ' '],
            [' ', 'X', ' '],
            [' ', ' ', ' ']
        ]
        list of lists of strs

        return namedtuple with x and y attrs (best move coordinates)
        """

        field = TicTacToeField(field=field_)
        if field.move_count == 0:
            return Point(GameStatus.IN_PROGRESS, randrange(0, 3), randrange(0, 3))
        if field.move_count >= 9:
            raise ValueError('game already ended')

        return TicTacToeAi.__move(field)

    @staticmethod
    def __move(field:TicTacToeField, level=0):
        if level > 2:
            return Point(GameStatus.IN_PROGRESS, -1, -1)
        
        win_status = GameStatus.O_WIN if field.move_count % 2 else GameStatus.X_WIN
        lose_status = GameStatus.X_WIN if field.move_count % 2 else GameStatus.O_WIN

        points = TicTacToeAi.__statuses_from_field(field)
        TicTacToeAi.__sort_points_statuses(points, win_status, lose_status)

        for point, i in zip(points, range(points.__len__())):
            if point.status == GameStatus.IN_PROGRESS:
                new_field = TicTacToeField(field.get())
                TicTacToeAi.__field_move(new_field, point.x, point.y)
                points[i] = Point(TicTacToeAi.__move(new_field, level+1).status, point.x, point.y)
            else:
                return point

        TicTacToeAi.__sort_points_statuses(points, win_status, lose_status)

        in_progress_count = 0
        for point in points:
            if point.status == GameStatus.IN_PROGRESS:
                in_progress_count += 1
            else:
                break
        if in_progress_count:
            return points[randrange(0, in_progress_count)]
        return points[0]
            

    @staticmethod
    def __field_move(field:TicTacToeField, x, y):
        if field.move_count % 2:
            field.move_O(x, y)
        else:
            field.move_X(x, y)

    @staticmethod
    def __if_move(field_:TicTacToeField, x, y) -> GameStatus:
        field = TicTacToeField(field_.get())
        TicTacToeAi.__field_move(field, x, y)
        return field.status

    @staticmethod
    def __statuses_from_field(field:TicTacToeField) -> list:
        points = []
        for row, y in zip(field.get(), range(TicTacToeAi.__field_size)):
            for symbol, x in zip(row, range(TicTacToeAi.__field_size)):
                if symbol == TicTacToeAi.__empty_cell_symbol:
                    status = TicTacToeAi.__if_move(field, x, y)
                    points.append(Point(status, x, y))
        return points

    @staticmethod
    def __sort_points_statuses(point_statuses:list, win_status, lose_status):
        def sort_key(x):
            if x.status == win_status:
                return 1
            elif x.status == GameStatus.DRAW:
                return 2
            elif x.status == GameStatus.IN_PROGRESS:
                return 3
            elif x.status == lose_status:
                return 4
            else:
                raise ValueError()
        point_statuses.sort(key=sort_key)

        

