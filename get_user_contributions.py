# import requests
import os
import re
import asyncio
import aiohttp
from pprint import pprint
from collections import defaultdict

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
NEXT_PATTERN = re.compile(r'(?<=<)([\S]*)(?=>; rel="next")', re.IGNORECASE)


async def get_contributors(
    repository_full_name: str, session: aiohttp.client.ClientSession = None
) -> list[str]:

    url = f"https://api.github.com/repos/{repository_full_name}/contributors"

    async with session.get(url) as response:
        print(response.status)
        if response.status in (204, 403, 404):
            return []
        if response.status != 200:
            print(response.status)
            raise Exception(response.content)

        contributors = await response.json()

        return [contrib["login"] for contrib in contributors]


async def get_repositories_by_user(
    user_name: str,
    results_per_page: int = 100,
    type: str = "all",
    session: aiohttp.client.ClientSession = None,
) -> list[str]:
    """curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    """
    url = f"https://api.github.com/users/{user_name}/repos?type={type}?&per_page={results_per_page}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    results = []
    async with session.get(url, headers=headers) as response:
        print(response.status)
        if response.status in (204, 403, 404):
            return []

        if response.status != 200:
            print(response.status)
            raise Exception(response.content)
        results.extend(await response.json())
        header = response.headers.get("Link", "")
        next_link = NEXT_PATTERN.search(header)

        while next_link:
            async with session.get(next_link.group(0), headers=headers) as response:
                results.extend(await response.json())
                header = response.headers.get("Link")
                next_link = NEXT_PATTERN.search(header)

        return [repo["full_name"] for repo in results if not repo["fork"]]

# start state: user
#start_state  = ['tobiadefami']
# goal_state = ["..,", 'linustorvalds']


async def get_collaborators(
    user_name: str, session: aiohttp.client.ClientSession = None
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)
    repository_full_names = await get_repositories_by_user(user_name, session=session)
    for repository_full_name in repository_full_names:
        contributors = await get_contributors(repository_full_name, session=session)
        for contributor in contributors:
            result[contributor].add(repository_full_name)
    
    return result




async def main(user_name: str):

    async with aiohttp.ClientSession() as session:
        repositories = await get_collaborators(user_name, session)
    pprint(repositories)


if __name__ == "__main__":
    asyncio.run(main("hwchase17"))
