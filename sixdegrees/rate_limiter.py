import asyncio
import time


class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = asyncio.Queue(maxsize=max_requests)

    async def wait(self):
        if self.requests.full():
            # Calculate the required sleep time by checking the timestamp of the oldest request
            oldest_request_time = await self.requests.get()
            sleep_time = self.period - (
                asyncio.get_event_loop().time() - oldest_request_time
            )
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        # Put the current request timestamp in the queue
        await self.requests.put(asyncio.get_event_loop().time())
        
    @staticmethod
    async def handle_rate_limit(response):
        rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', time.time()))  # Unix epoch time
        sleep_duration = rate_limit_reset - int(time.time()) + 5  # Sleep a bit longer than the reset time
        print(f"Rate limit hit. Sleeping for {sleep_duration} seconds.")
        await asyncio.sleep(sleep_duration)
        return True  # Indicates a rate limit was handled
