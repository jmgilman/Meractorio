from typing import Optional

from loguru import logger
from pydantic import BaseModel, RootModel, TypeAdapter

from mercatorio.scraper import Scraper

BASE_URL = "https://play.mercatorio.io/api/towns"


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


class MarketItemDataHistory(BaseModel):
    """Represents the historical market data for a single item in a town."""

    avg: float
    high: float
    low: float
    last: float
    vol: int
    turn: int


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


class Towns:
    """A class for interacting with the towns API endpoint."""

    scraper: Scraper

    def __init__(self, scraper):
        self.scraper = scraper

    def all(self):
        """Get a list of all towns in the game."""
        response = self.scraper.get(BASE_URL)
        return TownsList.model_validate(response.json())

    def market(self, id) -> dict[str, MarketDataComplete]:
        """Get market data for a town.

        Args:
            id (int): The ID of the town

        Returns:
            MarketData: The market data for the town
        """
        response = self.scraper.get(f"{BASE_URL}/{id}/marketdata")

        try:
            market_data = MarketData.model_validate(response.json())
        except Exception as e:
            logger.error(f"Error getting market data for {id}: {e}")
            with open("error.json", "w") as f:
                f.write(response.text)
            return {}

        final_data = {}
        for item, info in market_data.items():
            response = self.scraper.get(f"{BASE_URL}/{id}/markets/{item}")

            try:
                details = MarketItemDataDetails.model_validate(response.json())
            except Exception as e:
                logger.error(f"Error getting market data for {id} - {item}: {e}")
                with open("error.json", "w") as f:
                    f.write(response.text)
                continue

            response = self.scraper.get(f"{BASE_URL}/{id}/markets/{item}/history")
            ta = TypeAdapter(list[MarketItemDataHistory])

            try:
                history = ta.validate_python(response.json())
            except Exception as e:
                logger.error(f"Error getting market history for {id} - {item}: {e}")
                with open("error.json", "w") as f:
                    f.write(response.text)
                continue

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

            final_data[item] = MarketDataComplete(
                price=info.price,
                last_price=info.last_price,
                average_price=info.average_price,
                moving_average=info.moving_average,
                highest_bid=info.highest_bid,
                lowest_ask=info.lowest_ask,
                volume=info.volume,
                bid_volume=bid_volume,
                ask_volume=ask_volume,
                avg_bid_price=avg_bid_price,
                avg_ask_price=avg_ask_price,
                avg_historical_volume=sum([entry.vol for entry in history[:6]]) / 6,
            )

        return final_data
