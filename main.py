import asyncio
import aiosqlite
import asyncclick as click
from pyairtable.formulas import match

from loguru import logger
from mercatorio.api.api import Api, TurnInProgressException
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operations import RegionsSync, TownsSync, TownsMarketSync
from mercatorio.scraper import Scraper

import datetime
import sys

BASE_NAME = "Raw Data"


@click.command()
@click.option(
    "--api-key",
    type=str,
    help="Airbase API key.",
    envvar="AIRBASE_API_KEY",
)
@click.option(
    "--auth-path",
    type=click.Path(exists=True),
    default="auth.json",
    help="Path to the file holding session state.",
    envvar="AUTH_PATH",
)
@click.option(
    "--cache-path",
    type=click.Path(),
    default="cache.db",
    help="Path to the cache database.",
    envvar="CACHE_PATH",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.", envvar="DEBUG")
async def main(api_key: str, auth_path: str, cache_path: str, debug: bool):
    """A simple CLI for scraping Mercatorio data."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level}</level> {message}",
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )

    logger.info("Initializing Airtable API client.")
    airtable = ApiClient(api_key, BASE_NAME)

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
        # RegionsSync(api, airtable, cache),
        TownsSync(api, airtable, cache),
        # TownsMarketSync(api, airtable, cache),
    ]

    while True:
        try:
            try:
                current_turn = await api.turn()
                logger.info("Current turn: {}", current_turn)
            except TurnInProgressException:
                logger.info("Turn still in progress.")
                await asyncio.sleep(60)
                continue

            sync_table = airtable.base.table("Sync")
            if not sync_table.first(formula=match({"turn": current_turn})):
                logger.info("Sync needed.")

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
            else:
                logger.info("No sync needed.")

            await asyncio.sleep(60)
        # except Exception as e:
        #     logger.exception(e)
        #     await asyncio.sleep(60)
        except asyncio.exceptions.CancelledError:
            logger.info("Exiting.")
            await safe_close(api.scraper)
            await safe_close(cache)
            break


async def safe_close(resource):
    """Safely close an asynchronous resource, handling any exceptions."""
    try:
        await resource.close()
    except Exception as e:
        logger.error("Failed to close resource {}: {}", resource, str(e))


if __name__ == "__main__":
    main()
