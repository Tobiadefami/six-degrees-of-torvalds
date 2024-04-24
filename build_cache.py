import asyncio
import json
from typing import TypeAlias

import aiohttp
from sqlitedict import SqliteDict

from get_user_contributions import get_collaborators

User: TypeAlias = str
Repo: TypeAlias = str
Pair: TypeAlias = tuple[User, list[Repo] | None]
Path: TypeAlias = list[Pair]
PathMap: TypeAlias = dict[User, Path]


async def build_cache(session: aiohttp.ClientSession, depth: int = 3) -> PathMap:
    with SqliteDict("cache.sqlite", autocommit=True) as paths:
        # Try to resume from existing frontier, otherwise begin from the beginning
        if "__frontier__" not in paths:
            print("Resetting frontier...")
            paths["__frontier__"] = [[("torvalds", None)]]

        while paths["__frontier__"]:
            frontier = list(paths["__frontier__"])
            current_path = frontier.pop(0)
            paths["__frontier__"] = frontier

            user, _ = current_path[-1]
            collabs = await get_collaborators(user, session=session)
            new_paths = [
                current_path + [(collaborator, list(repos))]
                for collaborator, repos in collabs.items()
            ]

            for new_path in new_paths:
                last_state = new_path[-1]
                user, _ = last_state
                if user not in paths:
                    paths[user] = new_path

                    if len(new_path) <= depth:
                        frontier.append(new_path)
                        paths["__frontier__"] = frontier

            print(f"Visited users: {len(paths)}")
            print(f"Frontier size: {len(paths['__frontier__'])}")

    return paths


async def main():
    async with aiohttp.ClientSession() as session:
        await build_cache(session)


if __name__ == "__main__":
    asyncio.run(main())
