import asyncio
import os
import re
from collections import defaultdict
from pprint import pprint
from sixdegrees.contributions_from_events import (
    get_user_events,
    extract_repos_from_events,
)
import aiohttp

from sixdegrees.rate_limiter import RateLimiter

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
NEXT_PATTERN = re.compile(r'(?<=<)([\S]*)(?=>; rel="next")', re.IGNORECASE)

rate_limiter = RateLimiter(max_requests=900, period=60)

EXCLUDE = {"gitter-badger", "dependabot[bot]", "renovate[bot]"}


async def get_contributors(
    repository_full_name: str,
    session: aiohttp.client.ClientSession = None,
    max_retries: int = 3,
    delay: float = 1.0,
    access_token: str = None,
) -> list[str]:

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repository_full_name}/contributors"
    await rate_limiter.wait()

    attempt = 0
    while attempt < max_retries:
        try:
            async with session.get(url, headers=headers) as response:
                print(f"Get contributors for {repository_full_name}: {response.status}")
                if response.status == 200:
                    contributors = await response.json()
                    return [
                        contrib["login"]
                        for contrib in contributors
                        if contrib["login"] not in EXCLUDE
                    ]

                if response.status in (403,):
                    json_response = await response.json()
                    if "too large" in json_response.get("message"):
                        return await get_recent_committers(
                            repository_full_name, session, access_token=access_token
                        )
                    if "rate limit" in json_response.get("message", ""):
                        await RateLimiter.handle_rate_limit(response)
                        continue
                    return []

                if response.status in (204, 403, 404, 451):
                    return []

                response.raise_for_status()  # will raise an HTTPException for non-200 status codes
        except aiohttp.ClientConnectionError as e:
            print(
                f"Connection closed, attempt {attempt + 1} of {max_retries}: {str(e)}"
            )
            attempt += 1
            await asyncio.sleep(delay * (2**attempt))  # Exponential backoff
        except Exception as e:
            print(f"An error occurred on attempt {attempt + 1}: {str(e)}")
            attempt += 1
            if attempt >= max_retries:
                raise  # Re-raise the last exception if all retries fail

    raise Exception("Max retries exceeded")


async def get_recent_committers(
    repository_full_name: str,
    session: aiohttp.client.ClientSession = None,
    access_token: str = None,
) -> list[str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    # TODO: check larger number of commits
    url = f"https://api.github.com/repos/{repository_full_name}/commits?per_page=100"
    await rate_limiter.wait()

    max_retries = 5  # maximum number of retries
    retry_count = 0
    backoff_factor = 2  # exponential backoff factor

    while True:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:

                    print(
                        f"Get recent committers for {repository_full_name}: {response.status}"
                    )
                    commits = await response.json()

                    contributors = set()
                    for commit in commits:
                        login = (commit.get("author") or {}).get("login")
                        if login is None:
                            login = (commit.get("committer") or {}).get("login")
                        if login is not None:
                            contributors.add(login)
                        return list(contributors)

                elif response.status == 403 or response.status == 429:
                    print(await response.json())
                    json_response = await response.json()
                    if "rate limit" in json_response.get("message", ""):
                        await RateLimiter.handle_rate_limit(response=response)
                        continue
                elif response.status in (204, 404, 451):
                    return []
                else:
                    response.raise_for_status()
                # if response.status != 200:
                #     print(response.status)
                #     raise Exception(response.content)
        except aiohttp.ClientConnectionError as e:
            print(
                f"Error getting recent committers for {repository_full_name}: {str(e)}"
            )
            if retry_count < max_retries:
                sleep_time = backoff_factor**retry_count
                print(
                    f"Retrying in {sleep_time} seconds due to connection error: {str(e)}"
                )
                await asyncio.sleep(sleep_time)
                retry_count += 1
                continue
            else:
                print(f"Max retries reached for {repository_full_name}")
                return []
        except aiohttp.ClientResponseError as e:
            print(
                f"Error getting recent committers for {repository_full_name}: {str(e)}"
            )
            if retry_count < max_retries:
                sleep_time = backoff_factor**retry_count
                print(
                    f"Retrying in {sleep_time} seconds due to response error: {str(e)}"
                )
                await asyncio.sleep(sleep_time)
                retry_count += 1
                continue
            else:
                print(f"Max retries reached for {repository_full_name}")
                return []
        except Exception as e:
            print(
                f"Error getting recent committers for {repository_full_name}: {str(e)}"
            )
            return []


async def get_repositories_by_user(
    user_name: str,
    results_per_page: int = 100,
    type: str = "all",
    session: aiohttp.client.ClientSession = None,
    max_retries: int = 5,
    delay: float = 1.0,
    access_token: str = None,
) -> list[str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    await rate_limiter.wait()
    url = f"https://api.github.com/users/{user_name}/repos?type={type}?&per_page={results_per_page}"

    attempt = 0
    results = []

    events = await get_user_events(
        user_name, session=session, access_token=access_token
    )
    repos_from_events = await extract_repos_from_events(events)

    while attempt < max_retries:
        async with session.get(url, headers=headers) as response:
            try:
                print(f"Getting repos for {user_name}: {response.status}")
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
                try:
                    json_data = await response.json()
                    if isinstance(json_data, list):
                        results.extend(json_data)
                    else:
                        print("Unexpected json data", json_data)

                except Exception as e:
                    print("Error parsing json", str(e))
                    continue

                header = response.headers.get("Link", "")
                next_link = NEXT_PATTERN.search(header)

                while next_link:
                    try:
                        async with session.get(
                            next_link.group(0), headers=headers
                        ) as response:
                            json_data = await response.json()
                            if isinstance(json_data, list):
                                results.extend(json_data)
                            else:
                                print("Unexpected json data", json_data)

                            header = response.headers.get("Link")
                            next_link = NEXT_PATTERN.search(header)
                    except Exception as e:
                        print("Error getting next page", str(e))
                        continue
                repos = [
                    repo["full_name"]
                    for repo in results
                    if isinstance(repo, dict) and not repo.get("fork", True)
                ]
                print(f"Found repos: {repos}")
                for repository in repos_from_events:
                    if repository not in repos:
                        repos.append(repository)
                return repos

            except Exception as e:
                print(f"Error getting repos for {user_name}: {str(e)}")
                attempt += 1
                await asyncio.sleep(delay * (5**attempt))
                if attempt >= max_retries:
                    raise

    raise Exception("Max retries exceeded")


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
        repositories = await get_collaborators(
            user_name, session, access_token=GITHUB_API_KEY
        )
    pprint(repositories)


if __name__ == "__main__":
    asyncio.run(main("joshuafolorunsho"))
