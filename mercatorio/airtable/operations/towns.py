from mercatorio.airtable.operation import SyncOperation
from mercatorio.api import towns

TABLE_NAME = "Towns"


class TownsSync(SyncOperation):
    """Syncs town data from the Mercatorio API to AirTable."""

    def __init__(self, base_name: str, scraper, client):
        super().__init__(base_name, scraper, client)
        self.name = "Towns"

    def sync(self):
        api = towns.Towns(self.scraper)
        table = self._get_table(TABLE_NAME)

        data = []
        for town in api.all():
            data.append(
                {
                    "id": town.id,
                    "name": town.name,
                    "location_x": town.location.x,
                    "location_y": town.location.y,
                    "region": town.region,
                    "capital": town.capital,
                }
            )
        self.client.upsert_records_by_field(table, "id", data)
