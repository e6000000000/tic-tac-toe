from django.shortcuts import render, redirect, reverse
from .game_sessions import GameSessions


def game(request, session_id, player_id):
    """play game
    """
    game_session = GameSessions.get_by_id(session_id)
    if game_session.X_id == player_id:
        friend_player_id = game_session.O_id
    elif game_session.O_id == player_id:
        friend_player_id = game_session.X_id
    else:
        friend_player_id = 0
    friend_link = reverse('game_create') + f'{session_id}/{friend_player_id}'
    return render(request, 'game.html', {
        'friend_link': friend_link
    })

def game_create(request):
    """create game session
    """
    new_game_id = GameSessions.new()
    player_id = GameSessions.get_by_id(new_game_id).X_id
    return redirect('game', new_game_id, player_id)
