import os

from dotenv import load_dotenv
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.static import BASE_NAME, TABLE_DATA

load_dotenv()

airtable = ApiClient(os.environ["AIRBASE_API_KEY"], BASE_NAME)

for name, data in TABLE_DATA.items():
    table = next((t for t in airtable.base.tables() if t.name == name), None)
    if not table:
        airtable.base.create_table(name, data["fields"])
