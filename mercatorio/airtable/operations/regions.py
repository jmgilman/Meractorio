from mercatorio.airtable.operation import SyncOperation
from mercatorio.api import map

REGIONS_TABLE_NAME = "Regions"


class RegionsSync(SyncOperation):
    """Syncs region data from the Mercatorio API to AirTable."""

    def __init__(self, base_name: str, scraper, client):
        super().__init__(base_name, scraper, client)
        self.name = "Regions"

    def sync(self):
        map_api = map.Map(self.scraper)
        regions_table = self._get_table(REGIONS_TABLE_NAME)

        region_data = []
        for region in map_api.all():
            region_data.append(
                {
                    "id": region.id,
                    "name": region.name,
                    "center_x": region.center.x,
                    "center_y": region.center.y,
                    "size": region.size,
                }
            )
        self.client.upsert_records_by_field(regions_table, "id", region_data)
