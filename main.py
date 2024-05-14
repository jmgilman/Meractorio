import asyncio
import aiosqlite
import asyncclick as click
from dotenv import load_dotenv
from pyairtable.formulas import match
from pymerc.client import Client

from loguru import logger
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operations import RegionsSync, TownsSync, TownsMarketSync
from mercatorio.airtable.static import BASE_NAME

import datetime
import sys

load_dotenv()


@click.command()
@click.option(
    "--merc-api-user",
    type=str,
    help="Mercatorio API user.",
    envvar="MERC_API_USER",
)
@click.option(
    "--merc-api-token", type=str, help="Mercatorio API token.", envvar="MERC_API_TOKEN"
)
@click.option(
    "--airbase-api-key",
    type=str,
    help="Airbase API key.",
    envvar="AIRBASE_API_KEY",
)
@click.option(
    "--cache-path",
    type=click.Path(),
    default="cache.db",
    help="Path to the cache database.",
    envvar="CACHE_PATH",
)
@click.option("--debug", is_flag=True, help="Enable debug logging.", envvar="DEBUG")
async def main(
    merc_api_user: str,
    merc_api_token: str,
    airbase_api_key: str,
    cache_path: str,
    debug: bool,
):
    """A simple CLI for scraping Mercatorio data."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level}</level> {message}",
        level="DEBUG" if debug else "INFO",
        colorize=True,
    )

    logger.info("Initializing Mercatorio client.")
    client = Client(merc_api_user, merc_api_token)

    logger.info("Initializing Airtable API client.")
    airtable = ApiClient(airbase_api_key, BASE_NAME)

    logger.info("Loading cache from {}", cache_path)
    cache = await aiosqlite.connect(cache_path)

    # Define the operations to run.
    # Comment out any operations you don't want to run.
    operations = [
        RegionsSync(client, airtable, cache),
        TownsSync(client, airtable, cache),
        TownsMarketSync(client, airtable, cache),
    ]

    while True:
        try:
            try:
                current_turn = await turn(client)
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
        except Exception as e:
            logger.exception(e)
            await asyncio.sleep(60)
        except asyncio.exceptions.CancelledError:
            logger.info("Exiting.")
            await safe_close(cache)
            break


async def safe_close(resource):
    """Safely close an asynchronous resource, handling any exceptions."""
    try:
        await resource.close()
    except Exception as e:
        logger.error("Failed to close resource {}: {}", resource, str(e))


class TurnInProgressException(Exception):
    """Exception raised when a turn is in progress."""

    pass


async def turn(client: Client) -> int:
    """Get the current turn number.

    Args:
        client (Client): The Mercatorio API client.

    Returns:
        int: The current turn number.
    """
    response = await client.get("https://play.mercatorio.io/api/clock")

    if "preparing next game-turn, try again in a few seconds" in response.text:
        raise TurnInProgressException("A turn is in progress")

    return response.json()["turn"]


if __name__ == "__main__":
    main()
