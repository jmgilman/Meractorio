from mercatorio.airtable.operation import SyncOperation

TABLE_NAME = "Regions"


class RegionsSync(SyncOperation):
    """Syncs region data from the Mercatorio API to AirTable."""

    async def sync(self):
        data = []
        for region in await self.api.map.get_all():
            data.append(
                {
                    "id": region.id,
                    "name": region.name,
                    "center_x": region.center.x,
                    "center_y": region.center.y,
                    "size": region.size,
                }
            )
        self.client.upsert_records_by_field(TABLE_NAME, "id", data)
        return len(data)

    def __str__(self):
        return "Regions"
