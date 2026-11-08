import pytest
import data_fetcher


@pytest.fixture(autouse=True)
def clear_cache():
    """Start every test with an empty response cache so tests don't share results."""
    data_fetcher.cache.clear()
    yield
    data_fetcher.cache.clear()
