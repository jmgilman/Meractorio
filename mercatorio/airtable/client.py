from pyairtable import Api as AirtableApi, Base, formulas, Table


class ApiClient:
    def __init__(self, api_key: str, base: str):
        self.client = AirtableApi(api_key)
        self.base = next((b for b in self.client.bases() if b.name == base))

    def upsert_records_by_field(
        self, table_name: str, key_field: str, data: dict[str, any]
    ):
        """Upserts records to the specified table in the AirTable base."""
        table = next((t for t in self.base.tables() if t.name == table_name))
        recordsToUpsert = []
        for record in data:
            recordsToUpsert.append(dict(fields=record))

        table.batch_upsert(recordsToUpsert, [key_field], typecast=True)
