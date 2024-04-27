import os
import sys
import asyncio
from loguru import logger
from mercatorio.airtable.client import ApiClient
from mercatorio.api.api import Api
from mercatorio.scraper import Scraper
import aiosqlite

BASE_NAME = "Raw Data"

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
    scraper = Scraper("auth.json")
    cache = await aiosqlite.connect("cache.db")
    api = Api(scraper, cache)
    await api.init_cache()
