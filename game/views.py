from django.shortcuts import render, redirect, reverse
from .game_sessions import GameSessions


def game(request, session_id, player_id):
    game_session = GameSessions.get_session_by_id(session_id)
    if game_session.player1_id == player_id:
        friend_player_id = game_session.player2_id
    elif game_session.player2_id == player_id:
        friend_player_id = game_session.player1_id
    else:
        friend_player_id = 0
    friend_link = reverse('game_create') + f'{session_id}/{friend_player_id}'
    return render(request, 'game.html', {
        'friend_link': friend_link
    })

def game_create(request):
    new_game_id = GameSessions.new_session()
    player_id = GameSessions.get_session_by_id(new_game_id).player1_id
    return redirect('game', new_game_id, player_id)
