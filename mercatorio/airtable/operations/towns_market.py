import asyncio

from aiodecorators import Semaphore
from loguru import logger

from mercatorio.airtable.operation import SyncOperation

TABLE_NAME = "Town Market Data"


class TownsMarketSync(SyncOperation):
    """Syncs town market data from the Mercatorio API to AirTable."""

    async def sync(self):
        all_towns = await self.api.towns.all()
        results = await asyncio.gather(
            *[self.fetch_town_market_data(town) for town in all_towns]
        )
        data = [item for sublist in results for item in sublist]

        logger.info(f"Upserting {len(data)} records to {TABLE_NAME}")
        self.client.upsert_records_by_field(TABLE_NAME, "id", data)
        return len(data)

    @Semaphore(10)
    async def fetch_town_market_data(self, town):
        """Fetches market data for a single town.

        Args:
            town (Town): The town to fetch market data for.

        Returns:
            list[dict]: The market data for the town.
        """
        logger.info(f"Syncing market data for {town.name}")
        market_data = await self.api.towns.marketdata(town.id)
        return [
            {
                "id": f"{town.name} - {item}",
                "town": town.id,
                "item_name": item,
                "price": market_data[item].price,
                "last_price": market_data[item].last_price,
                "average_price": market_data[item].average_price,
                "moving_average": market_data[item].moving_average,
                "highest_bid": market_data[item].highest_bid,
                "lowest_ask": market_data[item].lowest_ask,
                "volume": market_data[item].volume,
                "volume_prev_12": market_data[item].volume_prev_12,
                "bid_volume_10": market_data[item].bid_volume_10,
                "ask_volume_10": market_data[item].ask_volume_10,
            }
            for item in market_data
        ]

    def __str__(self):
        return "Town Market Data"
