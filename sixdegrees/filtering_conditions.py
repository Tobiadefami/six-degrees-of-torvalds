def filter_repos(repo):
    if not isinstance(repo, dict):
        return False
    conditions = [
        not repo.get("fork", True),
        # not repo.get("archived", True),
        # not repo.get("watchers", True)
    ]
    return all(conditions)
