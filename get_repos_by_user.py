import requests
import os
import pprint

GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")

def get_repositories_by_user(user_name: str) -> list:
    """
    curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/repos

    Args:
        user (str): _description_

    Returns:
        list: _description_
    """
    
    
    url = "https://api.github.com/graphql"
    headers = {
        # "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        # "X-GitHub-Api-Version": "2022-11-28"
    }
    
    body = {
        "query": f"""query{{
            user(login: "{user_name}") {{
              name
              contributionsCollection {{
                commitContributionsByRepository{{
                    repository {{
                        nameWithOwner
                    }}
                }}
              }}
            }}
        }}"""
    }
    

    response = requests.post(url, headers=headers, json=body)
    # import ipdb; ipdb.set_trace()
    pprint.pprint(response.json())


if __name__ == "__main__":
    print(get_repositories_by_user("tobiadefami"))