from mercatorio.airtable.operation import SyncOperation
from mercatorio.api import map

TABLE_NAME = "Regions"


class RegionsSync(SyncOperation):
    """Syncs region data from the Mercatorio API to AirTable."""

    def __init__(self, base_name: str, scraper, client):
        super().__init__(base_name, scraper, client)
        self.name = "Regions"

    def sync(self):
        api = map.Map(self.scraper)
        table = self._get_table(TABLE_NAME)

        data = []
        for region in api.all():
            data.append(
                {
                    "id": region.id,
                    "name": region.name,
                    "center_x": region.center.x,
                    "center_y": region.center.y,
                    "size": region.size,
                }
            )
        self.client.upsert_records_by_field(table, "id", data)
