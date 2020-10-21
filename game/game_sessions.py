from .game_session import GameSession
from .exceptions import IdException


class GameSessions():
    """static class-manager of game sessions

    Examples
    --------
    >>> session_id = GameSession.new()
    >>> game_session = GameSession.get_by_id(session_id)
    >>> GameSession.get_by_id(-1) #invalid session_id
    IdException: can't find session id=-1
    """
    sessions = {}
    sessions_count = 0

    @staticmethod
    def new() -> int:
        """
        create new GameSession, return session id
        """
        GameSessions.sessions_count += 1
        GameSessions.sessions[GameSessions.sessions_count] = GameSession()
        return GameSessions.sessions_count

    @staticmethod
    def get_by_id(session_id:int) -> GameSession:
        try:
            return GameSessions.sessions[session_id]
        except:
            raise IdException(f'can\'t find session id={session_id}')
