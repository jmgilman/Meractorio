from typing import Optional

from pydantic import BaseModel, RootModel

from mercatorio.scraper import Scraper

BASE_URL = "https://play.mercatorio.io/api/towns"


class MarketItemData(BaseModel):
    """Represents the market data for a single item in a town."""

    price: Optional[float] = None
    last_price: Optional[float] = None
    average_price: Optional[float] = None
    moving_average: Optional[float] = None
    highest_bid: Optional[float] = None
    lowest_ask: Optional[float] = None
    volume: int


class MarketData(RootModel):
    """Represents the market data for all items in a town."""

    root: dict[str, MarketItemData]

    def __getitem__(self, item):
        return self.root[item]

    def __setitem__(self, key, value):
        self.root[key] = value

    def __iter__(self):
        return iter(self.root)

    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()

    def items(self):
        return self.root.items()


class Location(BaseModel):
    """Represents the location of a town."""

    x: int
    y: int


class Town(BaseModel):
    """Represents a town in the game."""

    id: str
    name: str
    location: Location
    region: int
    capital: bool


class TownsList(RootModel):
    """Represents a list of towns in the game."""

    root: list[Town]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, position):
        return self.root[position]


class Towns:
    """A class for interacting with the towns API endpoint."""

    scraper: Scraper

    def __init__(self, scraper):
        self.scraper = scraper

    def all(self):
        """Get a list of all towns in the game."""
        response = self.scraper.session.get(BASE_URL)
        return TownsList.model_validate(response.json())

    def market(self, id) -> MarketData:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            MarketData: The market data for the town
        """
        response = self.scraper.session.get(f"{BASE_URL}/{id}/marketdata")
        return MarketData.model_validate(response.json())
