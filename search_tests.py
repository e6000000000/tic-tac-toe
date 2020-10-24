from threading import Thread
from time import sleep

from game.search import GameSearch

results = {}
def search(result_name, player_side):
    print(result_name, GameSearch.search(player_side).session_id)

def start_search(result_name, player_side):
    Thread(target=search, args=(result_name, player_side)).start()

start_search('one', 'x')
start_search('two', 'x')
start_search('one1', 'o')
start_search('two1', 'o')
