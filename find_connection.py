import asyncio
import aiohttp
from get_user_contributions import get_collaborators
from typing import TypeAlias
from load_cache import load_cache


User: TypeAlias = str
Repo: TypeAlias = str
Pair: TypeAlias = tuple[User, list[Repo] | None]
Path: TypeAlias = list[Pair]

start_state = [("tobiadefami", None)]
goal_state = ["kennyrich"]


CACHE: dict[User, Path] = load_cache()


async def is_goal(state: Path, goal_user: User = goal_state[0]):
    current_user = state[-1][0]
    if current_user == goal_user:
        return True
    if current_user in CACHE and goal_user in [pair[0] for pair in CACHE[current_user]]:
        return True
    return False


async def get_next_paths(current_path: Path):
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
    if user not in CACHE:
        return current_path
    return {"current_path": current_path, 
            "connection": CACHE[user]}

async def find_connection(start_state: Path):
    frontier = [start_state]
    visited: set[str] = set()
    print("frontier", frontier)
    while frontier:
        current_path = frontier.pop(0)
        current_user = current_path[-1][0]

        if await is_goal(current_path):
            return get_full_path(current_path)
        
        if current_user in visited:
            continue

        visited.add(current_user)

        next_paths = await get_next_paths(current_path)
        frontier.extend(next_paths)

    return "Path not found"


async def main(start_state: Path = start_state):
    connection = await find_connection(start_state)
    print(connection)


if __name__ == "__main__":
    asyncio.run(main())
