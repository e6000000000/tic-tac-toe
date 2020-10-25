import asyncio

from game.search import GameSearch


async def search(result_name, player_side):
    result = await GameSearch.search(player_side)
    print(result_name, result.session_id, result.player_id)

tasks = []
async def main():
    tasks.append(asyncio.create_task(search('X1', 'x')))
    tasks.append(asyncio.create_task(search('X2', 'x')))
    tasks.append(asyncio.create_task(search('O1', 'o')))
    tasks.append(asyncio.create_task(search('O2', 'o')))

    for task in tasks:
        await task

asyncio.run(main())
