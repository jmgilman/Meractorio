from abc import ABC, abstractmethod

from mercatorio.airtable.client import ApiClient
from mercatorio.api.api import Api
from mercatorio.cache import Cache
from mercatorio.scraper import Scraper


class SyncOperation(ABC):
    """Represents a sync operation between the Mercatorio API and AirTable."""

    api: Api
    base_name: str
    cache: Cache
    client: ApiClient

    def __init__(self, api: Api, client: ApiClient, cache: Cache):
        self.api = api
        self.client = client
        self.cache = cache

    @abstractmethod
    async def sync(self):
        """Sync data from the Mercatorio API to AirTable."""
        pass
