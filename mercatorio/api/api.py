from mercatorio.api.endpoints.map import Map
from mercatorio.api.endpoints.towns import Towns
from mercatorio.cache import Cache
from mercatorio.scraper import Scraper


class Api:
    """A class for interacting with the Mercatorio API."""

    map: Map
    towns: Towns

    def __init__(self, scraper: Scraper, cache: Cache):
        self.map = Map(scraper, cache)
        self.towns = Towns(scraper, cache)

    async def init_cache(self):
        await self.towns.init_cache()
