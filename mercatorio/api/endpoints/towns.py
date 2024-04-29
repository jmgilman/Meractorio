import json
from typing import Optional

import asyncio
from loguru import logger
from pydantic import BaseModel, RootModel, TypeAdapter

from mercatorio.api.base import BaseAPI
from mercatorio.api.common import Location

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


class TownDomainStructure(BaseModel):
    id: str
    type: str
    tags: Optional[list[str]] = []


class TownDomain(BaseModel):
    owner_id: Optional[str] = None
    structure: Optional[TownDomainStructure] = None
    ask_price: Optional[str] = None


class TownStrucure(BaseModel):
    id: int
    type: str
    size: Optional[int] = 0
    owner_id: str
    location: Location
    land: Optional[list[Location]] = []


class TownDemand(BaseModel):
    product: str
    bonus: int
    desire: int
    request: int
    result: int


class TownCommoners(BaseModel):
    account_id: str
    count: int
    migration: float
    sustenance: list[TownDemand]


class TownGovernmentTaxes(BaseModel):
    land_tax: float
    structure_tax: float
    ferry_fees: float


class TownGovernment(BaseModel):
    account_id: str
    demands: list[TownDemand]
    taxes_collected: TownGovernmentTaxes


class TownChurch(BaseModel):
    project_ids: Optional[list[str]] = []


class TownCulture(BaseModel):
    special_market_pressure: Optional[dict[int, float]] = {}


class TownData(BaseModel):
    id: str
    name: str
    location: Location
    region: int
    center_ids: list[int]
    domain: dict[str, TownDomain]
    structures: dict[str, TownStrucure]
    household_ids: list[str]
    commoners: TownCommoners
    government: TownGovernment
    church: TownChurch
    navigation_zones: dict[int, int]
    culture: TownCulture


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

    async def data(self, id) -> TownData:
        """Get data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            TownData: The data for the town
        """
        response = await self.scraper.get(f"{BASE_URL}/{id}")

        try:
            town_data = TownData.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting data for town {id}: {e}")
            return {}

        return town_data

    async def marketdata(self, id) -> MarketData:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            MarketData: The market data for the town
        """
        logger.debug(f"Getting market data for town {id}")
        response = await self.scraper.get(f"{BASE_URL}/{id}/marketdata")

        try:
            market_data = MarketData.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting market data for {id}: {e}")
            return {}

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
