import asyncio
import json
from typing import TypeAlias

import aiohttp

from get_user_contributions import get_collaborators

User: TypeAlias = str
Repo: TypeAlias = str
Pair: TypeAlias = tuple[User, list[Repo] | None]
Path: TypeAlias = list[Pair]
PathMap: TypeAlias = dict[User, Path]


async def build_cache(session: aiohttp.ClientSession, depth: int = 2) -> PathMap:
    paths: PathMap = {}
    frontier: list[Path] = [[("torvalds", None)]]
    visited: set[User] = set()
    while frontier:
        current_path = frontier.pop(0)
        if (len(current_path) - 1) > depth:
            continue
        user, repos = current_path[-1]
        if user in visited:
            continue
        visited.add(user)
        print(f"Visited {len(visited)} users")
        if user not in paths:
            paths[user] = current_path
            collabs = await get_collaborators(user, session=session)
            frontier.extend(
                [
                    current_path + [(collaborator, list(repos))]
                    for collaborator, repos in collabs.items()
                ]
            )
    return paths


async def main():
    async with aiohttp.ClientSession() as session:
        paths = await build_cache(session)
        with open("cache.json", "w") as f:
            json.dump(paths, f)


if __name__ == "__main__":
    asyncio.run(main())
