import asyncio

from aiodecorators import Semaphore
from loguru import logger

from mercatorio.airtable.operation import SyncOperation
from mercatorio.api.endpoints.towns import Town

TABLE_NAME = "Towns"


class TownsSync(SyncOperation):
    """Syncs town data from the Mercatorio API to AirTable."""

    async def sync(self):
        all_towns = await self.api.towns.all()
        data = await asyncio.gather(*[self.fetch_town_data(town) for town in all_towns])

        logger.info(f"Upserting {len(data)} records to {TABLE_NAME}")
        self.client.upsert_records_by_field(TABLE_NAME, "id", data)
        return len(data)

    @Semaphore(10)
    async def fetch_town_data(self, town: Town):
        """Fetches data for a single town.

        Args:
            town (Town): The town to fetch data for.

        Returns:
            dict: The data for the town.
        """
        logger.info(f"Syncing town {town.name}")
        town_data = await self.api.towns.data(town.id)

        return {
            "id": town.id,
            "name": town.name,
            "location_x": town.location.x,
            "location_y": town.location.y,
            "region": town.region,
            "capital": town.capital,
            "commoners": town_data.commoners.count,
            "gentry": len(town_data.household_ids),
            "district": len(town_data.domain) - 1,
            "structures": len(town_data.structures),
            "total_taxes": sum(town_data.government.taxes_collected.__dict__.values()),
        }

    def __str__(self):
        return "Towns"
