from loguru import logger

from mercatorio.airtable.operation import SyncOperation
from mercatorio.api import towns

TABLE_NAME = "Town Market Data"


class TownsMarketSync(SyncOperation):
    """Syncs town market data from the Mercatorio API to AirTable."""

    def __init__(self, base_name: str, scraper, client, whitelist: list[str] = None):
        super().__init__(base_name, scraper, client)
        self.name = "Towns Market Data"
        self.whitelist = whitelist

    def sync(self):
        api = towns.Towns(self.scraper)
        table = self._get_table(TABLE_NAME)

        data = []
        all = api.all()
        if self.whitelist:
            all = [t for t in all if t.name in self.whitelist]

        for i, town in enumerate(all):
            logger.info(f"Syncing market data for {town.name} ({i + 1}/{len(all)})")
            for item, info in api.market(town.id).items():
                data.append(
                    {
                        "id": f"{town.name} - {item}",
                        "town": town.id,
                        "item_name": item,
                        "price": info.price,
                        "last_price": info.last_price,
                        "average_price": info.average_price,
                        "moving_average": info.moving_average,
                        "highest_bid": info.highest_bid,
                        "lowest_ask": info.lowest_ask,
                        "volume": info.volume,
                        "bid_volume": info.bid_volume,
                        "avg_bid_price": info.avg_bid_price,
                        "ask_volume": info.ask_volume,
                        "avg_ask_price": info.avg_ask_price,
                        "avg_historical_volume": info.avg_historical_volume,
                    }
                )

        logger.info(f"Upserting {len(data)} records to {TABLE_NAME}")
        self.client.upsert_records_by_field(table, "id", data)
