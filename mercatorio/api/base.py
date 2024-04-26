from mercatorio.cache import Cache
from mercatorio.scraper import Scraper


class BaseAPI:
    """A base class for interacting with the Mercatorio API."""

    def __init__(self, scraper: Scraper, cache: Cache):
        self.scraper = scraper
        self.cache = cache
