from sqlitedict import SqliteDict


def load_cache() -> dict[str, list[tuple[str, list[str]]]]:
    sqlite_cache: dict[str, list[tuple[str, list[str]]]] = {}
    with SqliteDict("sixdegrees/cache.sqlite") as paths:
        for key, value in paths.items():
            sqlite_cache[key] = value
    return sqlite_cache
