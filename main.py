import aiosqlite
import asyncclick as click

from loguru import logger
from pyairtable import Table
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
    airtable = ApiClient(os.environ["AIRTABLE_API_KEY"], BASE_NAME)

    logger.info("Loading auth data from {}", auth_path)
    scraper = Scraper(auth_path)

    logger.info("Loading cache from {}", cache_path)
    cache = await aiosqlite.connect(cache_path)

    api = Api(scraper, cache)
    await api.init_cache()

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
        # RegionsSync(api, airtable),
        # TownsSync(api, airtable),
        TownsMarketSync(api, airtable, cache, whitelist),
    ]

    sync_table = airtable.base.table("Sync")
    while True:
        current_turn = await api.turn()
        logger.info("Current turn: {}", current_turn)

        last_turn = sync_table.all()[-1]["fields"]["turn"]
        if last_turn < current_turn:
            num_records_synced = 0
            for op in operations:
                logger.info("Running sync operation: {}", op)
                num_records_synced += await op.sync()

            logger.info("Synced a total of {} records", num_records_synced)

            sync_table.create(
                {
                    "turn": current_turn,
                    "timestamp": datetime.datetime.now().isoformat() + "Z",
                    "records": num_records_synced,
                },
            )

            time.sleep(60)
        else:
            logger.info("No sync needed.")
            time.sleep(60)


if __name__ == "__main__":
    main()
