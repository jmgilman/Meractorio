from mercatorio.airtable.operation import SyncOperation
from mercatorio.api import towns

TOWNS_TABLE_NAME = "Towns"


class TownsSync(SyncOperation):
    """Syncs town data from the Mercatorio API to AirTable."""

    def __init__(self, base_name: str, scraper, client):
        super().__init__(base_name, scraper, client)
        self.name = "Towns"

    def sync(self):
        towns_api = towns.Towns(self.scraper)
        towns_table = self._get_table(TOWNS_TABLE_NAME)

        town_data = []
        for town in towns_api.all():
            town_data.append(
                {
                    "id": town.id,
                    "name": town.name,
                    "location_x": town.location.x,
                    "location_y": town.location.y,
                    "region": town.region,
                    "capital": town.capital,
                }
            )
        self.client.upsert_records_by_field(towns_table, "id", town_data)
