import requests
import os
from pprint import pprint


GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")


def get_repositories_by_user(user_name: str) -> list:
    """curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer <YOUR-TOKEN>" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    """
  
    url = f"https://api.github.com/users/{user_name}/repos?type=all?&per_page=100"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_API_KEY}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = requests.get(url, headers=headers)
    import ipdb; ipdb.set_trace()   
    pprint(response.json())
    
if __name__ == "__main__":
    get_repositories_by_user("tobiadefami")