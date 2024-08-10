import os
from sixdegrees.rate_limiter import RateLimiter
import aiohttp
import asyncio
import json
from collections import defaultdict
import logging
from typing import List, Dict, Any, Optional

GITHUB_TOKEN = os.getenv("GITHUB_API_KEY")
USERNAME = "torvalds"

rate_limiter = RateLimiter(max_requests=900, period=60)

events_to_include = ["PushEvent", "CreateEvent", "MemberEvent"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_user_events(
    username: str,
    per_page: int = 100,
    session: aiohttp.ClientSession = None,
    access_token: str|None = None,
) -> List[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    events = []
    page = 1
    event_types: Dict[str, set] = defaultdict(set)

    while True:
        logger.info(f"{page=}")
        url = f"https://api.github.com/users/{username}/events?per_page={per_page}&page={page}"
        await rate_limiter.wait()

        try:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Getting contributions for {username}: Page {page}, Status {response.status}")

                if response.status == 200:
                    data = await response.json()
                    if not data:
                        break  # No more data, exit the loop

                    events.extend(data)
                    for event in data:
                        event_types[event['type']].add(event['repo']['name'])

                    if len(data) < per_page:
                        break # last page is not full, so it is the final page

                    # # Check if there's a next page
                    # if 'Link' in response.headers:
                    #     if 'rel="next"' not in response.headers['Link']:
                    #         break  # No next page, exit the loop
                    # else:
                    #     break  # No Link header, assume no more pages

                    page += 1
                elif response.status == 422:
                    logger.info(f"Reached the end of available events for {username}")
                    break  # We've gone beyond the available pages, so stop

                elif response.status == 403:
                    json_response = await response.json()
                    if "rate limit" in json_response.get("message", "").lower():
                        await RateLimiter.handle_rate_limit(response=response)
                        continue
                    else:
                        logger.error(f"403 error: {json_response}")
                        break
                elif response.status in (204, 404):
                    logger.info(f"No events found for user {username}")
                    break
                else:
                    response.raise_for_status()

        except aiohttp.ClientError as e:
            logger.error(f"Error fetching events for {username}: {str(e)}")
            break

    logger.info(f"Collected {len(events)} events across {page} pages")
    logger.info(f"Event types collected: {dict(event_types)}")


    return events


async def extract_repos_from_events(events):
    repos = set()
    if events is None:
        return repos
    for event in events:
        # if event["type"] in events_to_include:
            repos.add(event["repo"]["name"])

    return repos


async def main():
    async with aiohttp.ClientSession() as session:
        events = await get_user_events(USERNAME, session=session, access_token=GITHUB_TOKEN)
        contributed_repos = await extract_repos_from_events(events)

    print(f"Repositories {USERNAME} has contributed to:")
    for repo in contributed_repos:
        print(repo)


if __name__ == "__main__":
    asyncio.run(main())
