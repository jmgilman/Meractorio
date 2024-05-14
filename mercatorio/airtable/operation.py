from abc import ABC, abstractmethod

from pymerc.client import Client

from mercatorio.airtable.client import ApiClient
from mercatorio.cache import Cache


class SyncOperation(ABC):
    """Represents a sync operation between the Mercatorio API and AirTable."""

    api: Client
    base_name: str
    cache: Cache
    client: ApiClient

    def __init__(self, api: Client, client: ApiClient, cache: Cache):
        self.api = api
        self.client = client
        self.cache = cache

    @abstractmethod
    async def sync(self) -> int:
        """Sync data from the Mercatorio API to AirTable.

        Returns:
            The number of records synced.
        """
        pass
