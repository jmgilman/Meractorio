from abc import ABC, abstractmethod

from mercatorio.airtable.client import ApiClient
from mercatorio.scraper import Scraper


class SyncOperation(ABC):
    """Represents a sync operation between the Mercatorio API and AirTable."""

    base_name: str
    client: ApiClient
    name: str
    scraper: Scraper

    def __init__(self, base_name: str, scraper: Scraper, client: ApiClient):
        self.base_name = base_name
        self.scraper = scraper
        self.client = client

    @abstractmethod
    def sync(self):
        """Sync data from the Mercatorio API to AirTable."""
        pass

    def _get_table(self, table_name: str):
        """Get a table by name."""
        base = self.client.base_by_name(self.base_name)
        return self.client.table_by_name(base, table_name)
