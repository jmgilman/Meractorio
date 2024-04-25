from pyairtable import Api as AirtableApi, Base, formulas, Table


class ApiClient:
    def __init__(self, api_key: str):
        self.client = AirtableApi(api_key)

    def base_by_name(self, name: str) -> Base:
        """Get a base by its name.

        Args:
            name (str): The name of the base.

        Returns:
            The base with the given name.
        """
        return next((b for b in self.client.bases() if b.name == name))

    def table_by_name(self, base: Base, name: str):
        """Get a table by its name.

        Args:
            base (Base): The base to search in.
            name (str): The name of the table.

        Returns:
            The table with the given name.
        """
        return next((t for t in base.tables() if t.name == name))

    def upsert_records_by_field(
        self, table: Table, key_field: str, data: dict[str, any]
    ):

        recordsToUpsert = []
        for record in data:
            recordsToUpsert.append(dict(fields=record))

        table.batch_upsert(recordsToUpsert, [key_field])
