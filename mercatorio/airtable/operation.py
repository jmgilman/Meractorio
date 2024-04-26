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

    def __init__(self, base_name: str, api: Api, client: ApiClient, cache: Cache):
        self.base_name = base_name
        self.api = api
        self.client = client
        self.cache = cache

    @abstractmethod
    async def sync(self):
        """Sync data from the Mercatorio API to AirTable."""
        pass

    def _get_table(self, table_name: str):
        """Get a table by name."""
        base = self.client.base_by_name(self.base_name)
        return self.client.table_by_name(base, table_name)
