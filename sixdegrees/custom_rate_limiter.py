from collections import defaultdict
import time


rate_limit: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT: int = 10  # 10 requests
TIME_WINDOW: int = 60  # 60 seconds


def is_rate_limited(user_id: str) -> bool:
    current_time: float = time.time()
    # Append the current time and filter out old requests
    rate_limit[user_id].append(current_time)
    rate_limit[user_id] = [
        t for t in rate_limit[user_id] if current_time - t < TIME_WINDOW
    ]
    # Check if the user exceeds the rate limit
    return len(rate_limit[user_id]) > RATE_LIMIT
