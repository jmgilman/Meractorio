import asyncio
from loguru import logger

from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operation import SyncOperation
from mercatorio.api.api import Api
from mercatorio.cache import Cache

TABLE_NAME = "Town Market Data"


class TownsMarketSync(SyncOperation):
    """Syncs town market data from the Mercatorio API to AirTable."""

    def __init__(
        self,
        api: Api,
        client: ApiClient,
        cache: Cache,
        whitelist: list[str] = None,
    ):
        super().__init__(api, client, cache)
        self.whitelist = whitelist

    async def sync(self):
        data = []
        all_towns = await self.api.towns.all()
        if self.whitelist:
            all_towns = [t for t in all_towns if t.name in self.whitelist]

        batch_size = 2
        data = []
        for i in range(0, len(all_towns), batch_size):
            batch = all_towns[i : i + batch_size]
            tasks = [self.fetch_town_data(town) for town in batch]
            results = await asyncio.gather(*tasks)
            data.extend(item for sublist in results for item in sublist)
            logger.info(
                f"Processed batch {i//batch_size + 1}/{(len(all_towns) + batch_size - 1) // batch_size}"
            )

        logger.info(f"Upserting {len(data)} records to {TABLE_NAME}")
        self.client.upsert_records_by_field(TABLE_NAME, "id", data)

    async def fetch_town_data(self, town):
        logger.info(f"Syncing market data for {town.name}")
        market_data = await self.api.towns.market(town.id)
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
                "bid_volume": market_data[item].bid_volume,
                "avg_bid_price": market_data[item].avg_bid_price,
                "ask_volume": market_data[item].ask_volume,
                "avg_ask_price": market_data[item].avg_ask_price,
                "avg_historical_volume": market_data[item].avg_historical_volume,
            }
            for item in market_data
        ]

    def __str__(self):
        return "Towns Market Data"
