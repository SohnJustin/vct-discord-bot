import httpx
import asyncio
import logging
from datetime import datetime
from cachetools import TTLCache

# Set up logging
logger = logging.getLogger(__name__)

# Base URL for the local vlr.gg API
BASE_URL = "http://127.0.0.1:3001"

# Cache for API responses (TTL 5 minutes)
cache = TTLCache(maxsize=100, ttl=300)


async def _get_cached(url: str) -> dict:
    """Fetch from API with caching."""
    if url in cache:
        logger.info(f"Cache hit for {url}")
        return cache[url]

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            data = resp.json()
            cache[url] = data
            logger.info(f"Fetched and cached {url}")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            raise


async def get_ongoing_games() -> dict:
    """Fetch ongoing/live games for NA region."""
    url = f"{BASE_URL}/v2/match?q=live_score"
    data = await _get_cached(url)
    # Filter for NA events
    if 'data' in data and 'segments' in data['data']:
        na_events = ['North America', 'Americas']
        filtered_segments = [
            seg for seg in data['data']['segments']
            if any(na in seg.get('match_event', '') for na in na_events)
        ]
        data['data']['segments'] = filtered_segments
    return data


async def get_previous_games(year: int = datetime.now().year) -> dict:
    """Fetch previous game results, filtered to the specified year."""
    url = f"{BASE_URL}/v2/match?q=results&region=na"
    data = await _get_cached(url)
    # Filter to current year (assuming data has 'date' or similar field)
    # Note: API may not have year filter, so basic filtering here
    if 'data' in data and 'segments' in data['data']:
        filtered = [match for match in data['data']
                    ['segments'] if str(year) in match.get('date', '')]
        data['data']['segments'] = filtered
    return data


async def get_future_games() -> dict:
    """Fetch upcoming games for NA region."""
    url = f"{BASE_URL}/v2/match?q=upcoming&region=na"
    return await _get_cached(url)


async def get_team_info(team_id: str) -> dict:
    """Fetch team information by ID."""
    url = f"{BASE_URL}/v2/team?id={team_id}"
    return await _get_cached(url)


async def get_player_info(player_id: str) -> dict:
    """Fetch player information by ID."""
    url = f"{BASE_URL}/v2/player?id={player_id}"
    return await _get_cached(url)

# Example usage (for testing)
if __name__ == "__main__":
    async def test():
        try:
            ongoing = await get_ongoing_games()
            print("Ongoing games:", ongoing)
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(test())
