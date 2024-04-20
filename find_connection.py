import asyncio

import aiohttp

from get_user_contributions import get_collaborators

Pair = tuple[str, set[str]]
Path = list[Pair]

start_state = [("ctmarinas", None)]
goal_state = ["torvalds"]


async def is_goal(state: Path):
    return state[-1][0] == goal_state[0]


async def get_next_paths(current_path: Path):
    last_user = current_path[-1][0]
    async with aiohttp.ClientSession() as session:
        collaborators = await get_collaborators(last_user, session=session)
        # import ipdb; ipdb.set_trace()
        next_paths = [
            current_path + [(collaborator, repos)]
            for collaborator, repos in collaborators.items()
        ]

    return next_paths


async def find_connection(start_state: Path):
    frontier = [start_state]
    visited: set[str] = set()

    while frontier:
        current_path = frontier.pop(0)
        if await is_goal(current_path):
            return current_path
        if current_path[-1][0] in visited:
            continue
        visited.add(current_path[-1][0])
        next_paths = await get_next_paths(current_path)
        frontier.extend(next_paths)

    return None


async def main(start_state: Path = start_state):
    print(start_state)
    connection = await find_connection(start_state)
    print(connection)


if __name__ == "__main__":
    asyncio.run(main())
