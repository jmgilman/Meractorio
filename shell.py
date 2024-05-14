import os
import sys

import aiosqlite
from dotenv import load_dotenv
from loguru import logger
from pymerc.client import Client

from mercatorio.airtable.client import ApiClient


BASE_NAME = "Raw Data"


load_dotenv()

logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level}</level> {message}",
    level="DEBUG",
    colorize=True,
)

# Define api and cache as global variables
airtable = None
api = None
cache = None


async def main():
    global airtable, api, cache

    airtable = ApiClient(os.environ["AIRBASE_API_KEY"], BASE_NAME)
    cache = await aiosqlite.connect("cache.db")
    api = Client(os.environ["MERC_API_USER"], os.environ["MERC_API_TOKEN"])
    await api.init_cache()
