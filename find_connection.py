import asyncio
import aiohttp
from get_user_contributions import get_collaborators
from typing import TypeAlias
from load_cache import load_cache


User: TypeAlias = str
Repo: TypeAlias = str
Pair: TypeAlias = tuple[User, list[Repo] | None]
Path: TypeAlias = list[Pair]

start_state = [("madisonmay", None)]
goal_state = ["torvalds"]


CACHE: dict[User, Path] = load_cache()


async def is_goal(state: Path, goal_user: User = goal_state[0]):
    current_user = state[-1][0]
    if current_user == goal_user:
        return True
    if current_user in CACHE:
        return True
    return False


async def get_next_paths(current_path: Path, session: aiohttp.ClientSession):
    last_user = current_path[-1][0]

    async with aiohttp.ClientSession() as session:
        collaborators = await get_collaborators(last_user, session=session)
        next_paths = [
            current_path + [(collaborator, repos)]
            for collaborator, repos in collaborators.items()
        ]

    return next_paths


def get_full_path(current_path):
    user = current_path[-1][0]
    data = current_path + CACHE[user][::-1]

    if user not in CACHE:
        return current_path
    import ipdb

    ipdb.set_trace()
    for item in range(len(data) - 2):
        if data[item][0] == data[item + 1][0]:
            data[item + 1] = (data[item + 2][0], data[item + 1][1])
    return [(repo, user) for (user, repo) in data[:-1]]


async def find_connection(start_state: Path):
    frontier = [start_state]
    visited: set[str] = set()
    print("frontier", frontier)

    async with aiohttp.ClientSession() as session:
        while frontier:
            current_path = frontier.pop(0)
            current_user = current_path[-1][0]

            if await is_goal(current_path):
                return get_full_path(current_path)

            if current_user in visited:
                continue

            visited.add(current_user)

            next_paths = await get_next_paths(current_path, session=session)
            frontier.extend(next_paths)

        return "Path not found"


async def main(start_state: Path = start_state):
    connection = await find_connection(start_state)
    print(connection)


if __name__ == "__main__":
    asyncio.run(main())
