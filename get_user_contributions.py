import requests
import os
import asyncio
import aiohttp
from pprint import pprint


GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")


async def get_repositories_by_user(
    user_name: str, results_per_page: int = 30, type: str = "all"
) -> list:
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
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                return []
            result = []
            repositories = await response.json()
            for repo in repositories:
                user_url = repo["owner"]["url"]
                async with session.get(user_url, headers=headers) as user_response:
                    user_data = await user_response.json()
                    repo_data = {
                        "repository_name": repo["full_name"],
                        "repository_id": repo["id"],
                        "user_data": user_data
                    }
                    result.append(repo_data)
                   
            return result[:5]


async def main(user_name: str):
    repositories = await get_repositories_by_user(user_name)
    pprint(repositories)


if __name__ == "__main__":
    asyncio.run(main("tobiadefami"))
