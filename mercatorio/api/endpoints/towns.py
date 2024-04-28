import json
from typing import Optional

import asyncio
from loguru import logger
from pydantic import BaseModel, RootModel, TypeAdapter

from mercatorio.api.base import BaseAPI

BASE_URL = "https://play.mercatorio.io/api/towns"


class ItemOrder(BaseModel):
    """Represents an order for an item in the market."""

    volume: int
    price: float


class MarketItemData(BaseModel):
    """Represents the market data for a single item in a town."""

    price: Optional[float] = 0.0
    last_price: Optional[float] = 0.0
    average_price: Optional[float] = 0.0
    moving_average: Optional[float] = 0.0
    highest_bid: Optional[float] = 0.0
    lowest_ask: Optional[float] = 0.0
    volume: int
    volume_prev_12: Optional[int] = 0
    bid_volume_10: Optional[int] = 0
    ask_volume_10: Optional[int] = 0


class MarketItemDataDetails(BaseModel):
    """Represents the market data for a single item in a town."""

    id: int
    product: str
    asset: str
    currency: str
    bids: list[ItemOrder]
    asks: list[ItemOrder]
    data: MarketItemData


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

    def __len__(self):
        return len(self.root)


class Towns(BaseAPI):
    """A class for interacting with the towns API endpoint."""

    volume_cache: dict[str, list[int]] = {}

    async def init_cache(self):
        pass

    async def all(self):
        """Get a list of all towns in the game."""
        response = await self.scraper.get(BASE_URL)
        return TownsList.model_validate(response.json())

    async def marketdata(self, id) -> MarketData:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            MarketData: The market data for the town
        """
        logger.debug(f"Getting market data for town {id}")
        market_data = await self.get_market_overview(id)
        if not market_data:
            return {}
        else:
            return market_data

    async def get_market_overview(self, town_id) -> Optional[MarketData]:
        """Get the market overview for a town.

        Args:
            town_id (int): The ID of the town

        Returns:
            MarketData: The market overview for the town
        """
        response = await self.scraper.get(f"{BASE_URL}/{town_id}/marketdata")

        try:
            market_data = MarketData.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting market data for {id}: {e}")
            return None

        return market_data

    async def get_market_item_overview(
        self, town_id, item
    ) -> Optional[MarketItemDataDetails]:
        """Get the market overview for an item in a town.

        Args:
            town_id (int): The ID of the town
            item (str): The item to get the overview for

        Returns:
            MarketItemDataDetails: The market overview for the town
        """
        response = await self.scraper.get(f"{BASE_URL}/{town_id}/markets/{item}")

        try:
            market_data = MarketItemDataDetails.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting market data for item {item} in {id}: {e}")
            return None

        return market_data
