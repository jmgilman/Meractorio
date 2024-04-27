import json
from typing import Optional

import asyncio
from loguru import logger
from pydantic import BaseModel, RootModel, TypeAdapter

from mercatorio.api.base import BaseAPI

BASE_URL = "https://play.mercatorio.io/api/towns"


class MarketItemVolumeData(BaseModel):
    """Represents the volume data for an item in a town."""

    bid_volume: float
    ask_volume: float
    avg_bid_price: float
    avg_ask_price: float


class MarketDataComplete(BaseModel):
    price: Optional[float] = 0.0
    last_price: Optional[float] = 0.0
    average_price: Optional[float] = 0.0
    moving_average: Optional[float] = 0.0
    highest_bid: Optional[float] = 0.0
    lowest_ask: Optional[float] = 0.0
    volume: int
    bid_volume: float
    ask_volume: float
    avg_bid_price: float
    avg_ask_price: float
    avg_historical_volume: float


class MarketItemData(BaseModel):
    """Represents the market data for a single item in a town."""

    price: Optional[float] = 0.0
    last_price: Optional[float] = 0.0
    average_price: Optional[float] = 0.0
    moving_average: Optional[float] = 0.0
    highest_bid: Optional[float] = 0.0
    lowest_ask: Optional[float] = 0.0
    volume: int


class ItemOrder(BaseModel):
    """Represents an order for an item in the market."""

    volume: int
    price: float


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
        await self.cache.execute(
            """
        CREATE TABLE IF NOT EXISTS item_volume_history (
            id TEXT PRIMARY KEY,
            volumes TEXT
        )
    """
        )
        await self.cache.commit()

    async def all(self):
        """Get a list of all towns in the game."""
        response = await self.scraper.get(BASE_URL)
        return TownsList.model_validate(response.json())

    async def market(self, id) -> dict[str, MarketDataComplete]:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            dict[str, MarketDataComplete]: The market data for the town
        """
        logger.debug(f"Loading cache for town {id}")
        await self.load_cache()

        logger.debug(f"Getting market overview for town {id}")
        market_data = await self.get_market_overview(id)
        if not market_data:
            return {}

        final_data = {}
        for item, info in market_data.items():
            logger.debug(f"Getting market data for {item} in town {id}")
            details = await self.get_market_item_overview(id, item)

            if not details:
                logger.error(f"Error getting market data for {item} in {id}")
                continue

            volume_data = self.parse_item_orders(details)
            avg_historical_volume = await self.calculate_volume_cached(
                id, item, info.volume
            )

            final_data[item] = MarketDataComplete(
                price=info.price,
                last_price=info.last_price,
                average_price=info.average_price,
                moving_average=info.moving_average,
                highest_bid=info.highest_bid,
                lowest_ask=info.lowest_ask,
                volume=info.volume,
                bid_volume=volume_data.bid_volume,
                ask_volume=volume_data.ask_volume,
                avg_bid_price=volume_data.avg_bid_price,
                avg_ask_price=volume_data.avg_ask_price,
                avg_historical_volume=avg_historical_volume,
            )

        logger.debug("Committing cache changes for town {id}")
        await self.cache.commit()

        return final_data

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

    def parse_item_orders(self, details: MarketItemDataDetails) -> MarketItemVolumeData:
        """Parse the item buy/sell order data from the details data.

        Args:
            details (MarketItemDataDetails): The details data to parse

        Returns:
            MarketItemVolumeData: The parsed volume data
        """
        if len(details.bids) > 0:
            bid_volume = sum([bid.volume for bid in details.bids])
            avg_bid_price = round(
                sum([bid.price for bid in details.bids]) / len(details.bids), 2
            )
        else:
            bid_volume = 0
            avg_bid_price = 0.0

        if len(details.asks) > 0:
            ask_volume = sum([ask.volume for ask in details.asks])
            avg_ask_price = round(
                sum([ask.price for ask in details.asks]) / len(details.asks), 2
            )
        else:
            ask_volume = 0
            avg_ask_price = 0.0

        return MarketItemVolumeData(
            bid_volume=bid_volume,
            ask_volume=ask_volume,
            avg_bid_price=avg_bid_price,
            avg_ask_price=avg_ask_price,
        )

    async def load_cache(self):
        """Load the volume cache from the cache."""
        async with self.cache.execute("SELECT * FROM item_volume_history") as cursor:
            rows = await cursor.fetchall()

            for id, volumes in rows:
                # Parse the JSON string into a Python list
                volumes_list = json.loads(volumes)
                self.volume_cache[id] = volumes_list

    async def calculate_volume_cached(
        self, town_id: int, item: str, cur_volume: int
    ) -> int:
        """Calculate the average volume for an item in a town.

        Args:
            town_id (int): The ID of the town
            item (str): The item to calculate the volume for
            cur_volume (int): The current volume for the item

        Returns:
            int: The average volume for the item
        """
        cache_id = self._get_cache_id(town_id, item)
        cached_volumes = self.volume_cache.get(cache_id, [])

        if not cached_volumes:
            cached_volumes = [cur_volume]
        elif len(cached_volumes) >= 6:
            cached_volumes.insert(0, cur_volume)
            cached_volumes.pop()
        else:
            cached_volumes.insert(0, cur_volume)

        logger.debug(
            f"Updating volume cache for {item} in town {town_id} to {cached_volumes}"
        )
        await self.cache.execute(
            "INSERT OR REPLACE INTO item_volume_history (id, volumes) VALUES (?, ?)",
            (cache_id, json.dumps(cached_volumes)),
        )

        return sum(cached_volumes) / len(cached_volumes)

    def _get_cache_id(self, town_id: int, item: str) -> str:
        """Generate a unique cache ID for the item data.

        Args:
            town_id (int): The ID of the town
            item (str): The item to get the data for

        Returns:
            str: The cache ID
        """
        return f"{town_id}_{item}"
