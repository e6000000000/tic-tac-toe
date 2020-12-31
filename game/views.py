from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseNotFound

from tictactoe.settings import CHANNELS_URLCONF
from .Statistic import Statistic
from .game_session import GameSession
from .exceptions import IdException


def game(request, session_id, player_id):
    """play game
    """
    return render(request, 'game.html', {
        'ws_url': reverse('game_websocket', args=(session_id, player_id), urlconf=CHANNELS_URLCONF)
    })

def friend_game(request, session_id, player_id):
    """play game with a friend
    """
    try:
        game_session = GameSession.get_by_id(session_id)
    except IdException:
        return HttpResponseNotFound('<h2>game not available</h2>')

    if game_session.X_id == player_id:
        friend_player_id = game_session.O_id
    elif game_session.O_id == player_id:
        friend_player_id = game_session.X_id
    else:
        friend_player_id = 0
    friend_url = reverse('friend_game', args=(session_id, friend_player_id))
    return render(request, 'game.html', {
        'friend_url': friend_url,
        'ws_url': reverse('game_websocket', args=(session_id, player_id), urlconf=CHANNELS_URLCONF)
    })

def game_with_ai(request, play_side):
    """play game with ai
    """
    
    return render(request, 'game.html', {
        'friend_url': '',
        'ws_url': reverse('aigame_websocket', args=(play_side, ), urlconf=CHANNELS_URLCONF)
    })

def game_create(request, play_side):
    """create game session
    """
    new_game_session = GameSession()
    new_game_id = new_game_session.id
    if play_side.lower() == 'x':
        player_id = new_game_session.X_id
    elif play_side.lower() == 'o':
        player_id = new_game_session.O_id
    else:
        raise ValueError(f'play_side should be "X" or "O", not {play_side}')
    return redirect('friend_game', new_game_id, player_id)

def lobby(request):
    """lobby from where player start
    """
    return render(request, 'lobby.html', {
        'searchX_ws_url': reverse('search_websocket', args=('X', ), urlconf=CHANNELS_URLCONF),
        'searchO_ws_url': reverse('search_websocket', args=('O', ), urlconf=CHANNELS_URLCONF),
    })

def statistic(request):
    """send json with statistics
    """

    return HttpResponse(Statistic.as_json())
