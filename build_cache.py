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
        user, _ = current_path[-1]
        collabs = await get_collaborators(user, session=session)
        new_paths = [
            current_path + [(collaborator, list(repos))]
            for collaborator, repos in collabs.items()
        ]

        for new_path in new_paths:
            last_state = new_path[-1]
            user, _ = last_state
            if user not in visited:
                paths[user] = new_path
                visited.add(user)

                if len(new_path) <= depth:
                    frontier.append(new_path)

        print(f"Visited {len(visited)} users")

    return paths


async def main():
    async with aiohttp.ClientSession() as session:
        paths = await build_cache(session)
        with open("cache.json", "w") as f:
            json.dump(paths, f)


if __name__ == "__main__":
    asyncio.run(main())
