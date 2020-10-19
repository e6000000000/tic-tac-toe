from . import game_session
from .exceptions import IdException, MoveUnableException


class GameSessions():
    sessions = {}
    sessions_count = 0

    @staticmethod
    def new_session() -> int:
        """
        create new game batch, return game id
        """
        GameSessions.sessions_count += 1
        GameSessions.sessions[GameSessions.sessions_count] = game_session.GameSession()
        return GameSessions.sessions_count

    @staticmethod
    def get_session_by_id(session_id):
        try:
            return GameSessions.sessions[session_id]
        except:
            raise IdException(f'can\'t find session id={session_id}')
