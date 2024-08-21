import asyncio
import os
import re
from typing import Any, List, Dict
from collections import defaultdict
from pprint import pprint
from sixdegrees.contributions_from_events import (
    get_user_events,
    extract_repos_from_events,
)
import aiohttp
import logging
from sixdegrees.rate_limiter import RateLimiter
from sixdegrees.filtering_conditions import filter_repos
from cachetools import TTLCache


GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
NEXT_PATTERN = re.compile(r'(?<=<)([\S]*)(?=>; rel="next")', re.IGNORECASE)

rate_limiter = RateLimiter(max_requests=900, period=60)

EXCLUDE = {"gitter-badger", "dependabot[bot]", "renovate[bot]", "mergify[bot]"}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


contributors_cache = TTLCache(maxsize=100000, ttl=86400)
commiters_cache = TTLCache(maxsize=100000, ttl=86400)


async def get_contributors(
    repository_full_name: str,
    session: aiohttp.ClientSession,
    access_token: str,
    max_retries: int = 3,
    delay: float = 1.0
) -> List[str]:

    # Check cache first
    if repository_full_name in contributors_cache:
        logger.info(f"Using cached contributors for {repository_full_name}")
        return contributors_cache[repository_full_name]

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repository_full_name}/contributors?per_page=100"

    await rate_limiter.wait()

    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Get contributors for {repository_full_name}: {response.status}")

                if response.status == 200:
                    contributors_data = await response.json()
                    contributors = [
                        contrib["login"].lower()
                        for contrib in contributors_data
                        if contrib["login"] not in EXCLUDE
                    ]
                    contributors_cache[repository_full_name] = contributors
                    return contributors

                if response.status == 403:
                    json_response = await response.json()
                    if "too large" in json_response.get("message", ""):
                        return await get_recent_committers(repository_full_name, session, access_token)
                    if "rate limit" in json_response.get("message", ""):
                        await RateLimiter.handle_rate_limit(response)
                        continue

                if response.status in (204, 403, 404, 451):
                    return []

                response.raise_for_status()

        except aiohttp.ClientConnectionError as e:
            logger.error(f"Connection error, attempt {attempt + 1} of {max_retries}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (2**attempt))
            else:
                raise

        except Exception as e:
            logger.error(f"An error occurred on attempt {attempt + 1}: {str(e)}")
            if attempt >= max_retries - 1:
                raise

    raise Exception("Max retries exceeded")

async def get_recent_committers(
    repository_full_name: str,
    session: aiohttp.ClientSession,
    access_token: str,
    max_retries: int = 3,
    delay: float = 1.0
) -> List[str]:

    # Check cache first
    if repository_full_name in commiters_cache:
        logger.info(f"Using cached recent committers for {repository_full_name}")
        return commiters_cache[repository_full_name]

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repository_full_name}/commits?per_page=100"

    await rate_limiter.wait()

    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Get recent committers for {repository_full_name}: {response.status}")

                if response.status == 200:
                    commits = await response.json()
                    contributors = set()
                    for commit in commits:
                        login = (commit.get("author") or {}).get("login")
                        if login is None:
                            login = (commit.get("committer") or {}).get("login")
                        if login is not None:
                            contributors.add(login.lower())
                    commiters_cache[repository_full_name] = list(contributors)
                    return list(contributors)

                elif response.status == 403 or response.status == 429:
                    json_response = await response.json()
                    if "rate limit" in json_response.get("message", ""):
                        await RateLimiter.handle_rate_limit(response)
                        continue

                elif response.status in (204, 404, 451):
                    return []

                response.raise_for_status()

        except aiohttp.ClientConnectionError as e:
            logger.error(f"Error getting recent committers for {repository_full_name}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (2**attempt))
                continue
            else:
                logger.info(f"Max retries reached for {repository_full_name}")
                return []

        except aiohttp.ClientResponseError as e:
            logger.error(f"Error getting recent committers for {repository_full_name}: {str(e)}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay * (2**attempt))
                continue
            else:
                logger.info(f"Max retries reached for {repository_full_name}")
                return []

        except Exception as e:
            logger.error(f"Error getting recent committers for {repository_full_name}: {str(e)}")
            return []

    raise Exception("Max retries exceeded")


# async def get_repositories_by_user(
#     user_name: str,
#     results_per_page: int = 100,
#     type: str = "all",
#     session: aiohttp.client.ClientSession = None,
#     max_retries: int = 5,
#     delay: float = 1.0,
#     access_token: str = None,
# ) -> list[str]:
#     headers = {
#         "Accept": "application/vnd.github+json",
#         "Authorization": f"Bearer {access_token}",
#         "X-GitHub-Api-Version": "2022-11-28",
#     }
#     await rate_limiter.wait()
#     url = f"https://api.github.com/users/{user_name}/repos?type={type}?&per_page={results_per_page}"

#     attempt = 0
#     results = []

#     events = await get_user_events(
#         user_name, session=session, access_token=access_token
#     )
#     repos_from_events = await extract_repos_from_events(events)

#     while attempt < max_retries:
#         async with session.get(url, headers=headers) as response:
#             try:
#                 logger.info(f"Getting repos for {user_name}: {response.status}")
#                 if response.status in (403,):
#                     json_response = await response.json()
#                     print(json_response)
#                     if "rate limit" in json_response.get("message", ""):
#                         await RateLimiter.handle_rate_limit(response=response)
#                         continue
#                 if response.status in (204, 403, 404):
#                     return []

#                 if response.status != 200:
#                     logger.info(response.status)
#                     raise Exception(response.content)
#                 try:
#                     json_data = await response.json()
#                     if isinstance(json_data, list):
#                         results.extend(json_data)
#                     else:
#                         logger.info("Unexpected json data", json_data)

#                 except Exception as e:
#                     logger.error("Error parsing json", str(e))
#                     continue

#                 header = response.headers.get("Link", "")
#                 next_link = NEXT_PATTERN.search(header)

#                 while next_link:
#                     try:
#                         async with session.get(
#                             next_link.group(0), headers=headers
#                         ) as response:
#                             json_data = await response.json()
#                             if isinstance(json_data, list):
#                                 results.extend(json_data)
#                             else:
#                                 logger.info("Unexpected json data", json_data)

#                             header = response.headers.get("Link")
#                             next_link = NEXT_PATTERN.search(header)
#                     except Exception as e:
#                         logger.error("Error getting next page", str(e))
#                         continue


#                 repos = [
#                     repo["full_name"]
#                     for repo in results
#                     if isinstance(repo, dict) and filter_repos(repo)
#                 ]
#                 print(f"Found repos: {repos}")
#                 for repository in repos_from_events:
#                     if repository not in repos:
#                         repos.append(repository)
#                 print(f"LENGTH OF REPOS {len(repos)}")
#                 return repos

#             except Exception as e:
#                 logger.error(f"Error getting repos for {user_name}: {str(e)}")
#                 attempt += 1
#                 await asyncio.sleep(delay * (5**attempt))
#                 if attempt >= max_retries:
#                     raise

#     raise Exception("Max retries exceeded")
#
async def get_repositories_by_user(
    user_name: str,
    session: aiohttp.ClientSession,
    access_token: str,
    max_repos: int = 1000,
    max_retries: int = 5,
    delay: float = 1.0
) -> List[str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    async def fetch_page(url: str) -> tuple[List[Dict[str, Any]], str | None]:
        await rate_limiter.wait()
        attempt = 0
        while attempt < max_retries:
            try:
                async with session.get(url, headers=headers) as response:
                    logger.info(f"Fetching repos page for {user_name}: {response.status}")
                    if response.status == 200:
                        repos = await response.json()
                        links = response.links
                        next_url = links.get('next', {}).get('url')
                        return repos, next_url
                    elif response.status in (403, 429):
                        json_response = await response.json()
                        if "rate limit" in json_response.get("message", ""):
                            await RateLimiter.handle_rate_limit(response)
                            continue
                    elif response.status in (204, 404):
                        return [], None
                    else:
                        response.raise_for_status()
            except aiohttp.ClientConnectionError as e:
                logger.error(f"Connection error, attempt {attempt + 1} of {max_retries}: {str(e)}")
                attempt += 1
                await asyncio.sleep(delay * (2**attempt))  # Exponential backoff
            except Exception as e:
                logger.error(f"Error fetching repos page, attempt {attempt + 1}: {str(e)}")
                attempt += 1
                if attempt >= max_retries:
                    raise
                await asyncio.sleep(delay * (2**attempt))
        raise Exception("Max retries exceeded")

    async def fetch_all_pages() -> List[Dict[str, Any]]:
        all_repos = []
        next_url = f"https://api.github.com/users/{user_name}/repos?type=all&per_page=100"

        while next_url:
            repos, next_url = await fetch_page(next_url)
            all_repos.extend(repos)

        filtered_repos = [
                repo["full_name"]
                for repo in all_repos
                if isinstance(repo, dict) and filter_repos(repo)
            ]
        return filtered_repos

    filtered_repos = await fetch_all_pages()

    events = await get_user_events(user_name, session=session, access_token=access_token)
    repos_from_events = await extract_repos_from_events(events)

    for repository in repos_from_events:
        if repository not in filtered_repos:
            filtered_repos.append(repository)
    print(f"LENGTH OF FOUND REPOS: {len(filtered_repos)}")
    logger.info(f"Found {len(filtered_repos)} repos for {user_name}")
    return filtered_repos

async def get_collaborators(
    user_name: str,
    session: aiohttp.ClientSession = None,
    access_token: str = None,
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = defaultdict(set)

    async def process_repository(repository_full_name: str):
        contributors = await get_contributors(
            repository_full_name, session=session, access_token=access_token
        )
        if user_name in contributors:
            for contributor in contributors:
                if contributor.lower() != user_name.lower():
                    result[contributor].add(repository_full_name)

    repository_full_names = await get_repositories_by_user(
        user_name, session=session, access_token=access_token
    )

    tasks = [process_repository(repo) for repo in repository_full_names]
    await asyncio.gather(*tasks)

    return result


async def main(user_name: str):
    async with aiohttp.ClientSession() as session:
        repositories = await get_repositories_by_user(
            user_name, session=session, access_token=GITHUB_API_KEY
        )
    pprint(repositories)


if __name__ == "__main__":
    asyncio.run(main("mattn"))
