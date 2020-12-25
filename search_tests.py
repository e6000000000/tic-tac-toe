import asyncio

from game.search import GameSearch

searchs = []
async def search(result_name, player_side):
    game_search = GameSearch(player_side)
    searchs.append(game_search)
    result = await game_search.search()
    print(result_name, result.session_id, result.player_id)

async def cancel_search(result_name, search_index):
    await searchs[search_index].cancel_search()
    print(result_name, f'search with index {search_index} was canceled')

tasks = []
async def main():
    tasks.append(asyncio.create_task(search('X1', 'x')))
    tasks.append(asyncio.create_task(search('X2', 'x')))
    tasks.append(asyncio.create_task(search('O1', 'o')))
    tasks.append(asyncio.create_task(cancel_search('X2', 1)))
    tasks.append(asyncio.create_task(search('O2', 'o')))

    for task in tasks:
        await task
        await asyncio.sleep(0.5)

asyncio.run(main())
