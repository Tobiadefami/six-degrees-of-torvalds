import os
from sixdegrees.rate_limiter import RateLimiter
import aiohttp
import asyncio

GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")
USERNAME = "madisonmay"


rate_limiter = RateLimiter(max_requests=900, period=60)

events_to_include = ["PushEvent", "CreateEvent", "MemberEvent"]


async def get_user_events(
    username: str,
    per_page: int = 100,
    session: aiohttp.client.ClientSession = None,
    access_token: str = None,
):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    events = []
    page = 1
    url = f"https://api.github.com/users/{username}/events?per_page={per_page}&page={page}"
    await rate_limiter.wait()

    while True:
        async with session.get(url, headers=headers) as response:
            print(f"Getting contributions for {username}: {response.status}")
            data = await response.json()

            if not data:
                break

            if response.status in (403,):
                json_response = await response.json()
                print(json_response)
                if "rate limit" in json_response.get("message", ""):
                    await RateLimiter.handle_rate_limit(response=response)
                    continue
            if response.status in (204, 403, 404):
                return []

            if response.status != 200:
                print(response.status)
                raise Exception(response.content)
            if response.status == 422:
                print(
                    f"Stopping pagination: received 422 Unprocessable Entity at page {page}"
                )
                break
            response.raise_for_status()

            events.extend(data)
            page += 1

            return events


async def extract_repos_from_events(events):
    repos = set()
    if events is None:
        return repos
    for event in events:
        if event["type"] in events_to_include:
            repos.add(event["repo"]["name"])
    return repos


async def main():
    async with aiohttp.ClientSession() as session:
        events = await get_user_events(USERNAME, session=session)
        contributed_repos = await extract_repos_from_events(events)

    print(f"Repositories {USERNAME} has contributed to:")
    for repo in contributed_repos:
        print(repo)


if __name__ == "__main__":
    asyncio.run(main())
