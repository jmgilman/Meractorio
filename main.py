import asyncclick as click

from loguru import logger
from mercatorio.api.api import Api
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operations import RegionsSync, TownsSync, TownsMarketSync
from mercatorio.cache import Cache
from mercatorio.scraper import Scraper

import datetime
import os
import sys
import time

BASE_NAME = "Raw Data"


@click.command()
@click.option(
    "--auth-path",
    type=click.Path(exists=True),
    default="auth.json",
    help="Path to the file holding session state.",
)
@click.option(
    "--cache-path",
    type=click.Path(),
    default="cache.db",
    help="Path to the cache database.",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.")
async def main(auth_path: str, cache_path: str, debug: bool):
    """A simple CLI for scraping Mercatorio data."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level}</level> {message}",
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )

    if not os.environ.get("AIRTABLE_API_KEY"):
        logger.error("AIRTABLE_API_KEY environment variable is not set.")
        sys.exit(1)

    logger.info("Initializing Airtable API client.")
    airtable = ApiClient(os.environ["AIRTABLE_API_KEY"])

    logger.info("Loading auth data from {}", auth_path)
    scraper = Scraper(auth_path)

    logger.info("Loading cache from {}", cache_path)
    cache = Cache(cache_path)
    await cache.init()

    api = Api(scraper, cache)

    # Town whitelist for market data (speeds up syncing)
    whitelist = [
        "Eindburg",
        "Magdedorf",
        "Antbrücken",
        "Antstock",
        "Hambeck",
        "Livertal",
        "Nürnend",
        "Eshagen",
        "Swinfield",
        "Blacknieder",
    ]

    # Define the operations to run.
    # Comment out any operations you don't want to run.
    operations = [
        # RegionsSync(BASE_NAME, scraper, api),
        # TownsSync(BASE_NAME, scraper, api),
        TownsMarketSync(BASE_NAME, api, airtable, whitelist),
    ]

    while True:
        for op in operations:
            logger.info("Running sync operation: {}", op)
            await op.sync()

        now = datetime.datetime.now()
        seconds_until_next_hour = (60 - now.minute) * 60 - now.second
        seconds_to_sleep = seconds_until_next_hour + 60
        logger.info("Sleeping for {} seconds", seconds_to_sleep)
        time.sleep(seconds_to_sleep)


if __name__ == "__main__":
    main()
