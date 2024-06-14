import asyncio
import aiohttp
import traceback
from typing import TypeAlias
from sqlitedict import SqliteDict
from sixdegrees.get_user_contributions import get_collaborators
import sqlitedict
import os

User: TypeAlias = str
Repo: TypeAlias = str
Pair: TypeAlias = tuple[User, list[Repo] | None]
Path: TypeAlias = list[Pair]
PathMap: TypeAlias = dict[User, Path]

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")


def initialize_frontier(paths: PathMap):
    try:
        if "__frontier__" not in paths:
            print("Resetting frontier...")
            paths["__frontier__"] = [[("torvalds", None)]]
    except Exception as e:
        print("Error initializing frontier", str(e))
        traceback.print_exc()


async def build_cache(
    session: aiohttp.ClientSession, depth: int = 6, retries=5, delay=1
) -> PathMap:
    attempts = 0

    while attempts < retries:
        try:
            with SqliteDict("cache.sqlite", autocommit=True) as paths:
                # Try to resume from existing frontier, otherwise begin from the beginning
                initialize_frontier(paths)

                while paths["__frontier__"]:
                    frontier = list(paths["__frontier__"])
                    current_path = frontier.pop(0)
                    paths["__frontier__"] = frontier

                    user, _ = current_path[-1]
                    collabs = await get_collaborators(
                        user, session=session, access_token=GITHUB_API_KEY
                    )
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

        except sqlitedict.sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("Database locked. Retrying...")
                attempts += 1
                await asyncio.sleep(delay * (2**attempts))

    raise Exception("Failed to build cache")


async def main():
    async with aiohttp.ClientSession() as session:
        await build_cache(session)


if __name__ == "__main__":
    asyncio.run(main())
