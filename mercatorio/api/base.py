from mercatorio.cache import Cache
from mercatorio.scraper import Scraper


class BaseAPI:
    """A base class for interacting with the Mercatorio API."""

    def __init__(self, scraper: Scraper, cache: Cache):
        self.scraper = scraper
        self.cache = cache

    def init_cache(self):
        """Initialize the cache for this API endpoint."""
        pass
