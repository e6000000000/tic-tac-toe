from django.shortcuts import render, redirect, reverse
from .game_sessions import GameSessions
import asyncio


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
    friend_url = reverse('lobby') + f'{session_id}/{friend_player_id}'
    return render(request, 'game.html', {
        'friend_url': friend_url,
        'ws_url': f'/ws/{session_id}/{player_id}' #need to be redesigned
    })

def game_with_ai(request, play_side):
    """play game with ai
    """
    
    return render(request, 'game.html', {
        'friend_url': '',
        'ws_url': f'/aiws/{play_side}' #need to be redesigned
    })

def game_create(request, play_side):
    """create game session
    """
    new_game_id = GameSessions.new()
    if play_side.lower() == 'x':
        player_id = GameSessions.get_by_id(new_game_id).X_id
    elif play_side.lower() == 'o':
        player_id = GameSessions.get_by_id(new_game_id).O_id
    else:
        raise ValueError(f'play_side should be "X" or "O", not {play_side}')
    return redirect('game', new_game_id, player_id)

def lobby(request):
    """lobby from where player start
    """
    return render(request, 'lobby.html', {
        'search_ws_base_url': f'/searchws' #need to be redesigned
    })
