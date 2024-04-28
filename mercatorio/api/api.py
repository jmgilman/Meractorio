from mercatorio.api.endpoints.map import Map
from mercatorio.api.endpoints.towns import Towns
from mercatorio.cache import Cache
from mercatorio.scraper import Scraper


class TurnInProgressException(Exception):
    """Exception raised when a turn is in progress."""

    pass


class Api:
    """A class for interacting with the Mercatorio API."""

    map: Map
    scraper: Scraper
    towns: Towns

    def __init__(self, scraper: Scraper, cache: Cache):
        self.scraper = scraper
        self.map = Map(scraper, cache)
        self.towns = Towns(scraper, cache)

    async def init_cache(self):
        """Initialize the cache for the API endpoints."""
        await self.towns.init_cache()

    async def turn(self) -> int:
        """Get the current turn number."""
        response = await self.scraper.get("https://play.mercatorio.io/api/clock")

        if "preparing next game-turn, try again in a few seconds" in response.text:
            raise TurnInProgressException("A turn is in progress")

        return response.json()["turn"]
