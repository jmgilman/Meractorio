import os

from dotenv import load_dotenv
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.static import TABLE_DATA

BASE_NAME = "Raw Data"
REGIONS_TABLE_NAME = "Regions"
TOWNS_TABLE_NAME = "Towns"
TOWN_MARKETS_TABLE_NAME = "Town Market Data"

load_dotenv()

airtable = ApiClient(os.environ["AIRBASE_API_KEY"], BASE_NAME)

for name, data in TABLE_DATA.items():
    table = next((t for t in airtable.base.tables() if t.name == name), None)
    if not table:
        airtable.base.create_table(name, data["fields"])
