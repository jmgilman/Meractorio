import click

from loguru import logger
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operations import RegionsSync, TownsSync, TownsMarketSync
from mercatorio.api import map, towns
from mercatorio.scraper import Scraper

import datetime
import os
import sys
import time

BASE_NAME = "Raw Data"


@click.command()
@click.option(
    "--state",
    type=click.Path(exists=True),
    default="state.json",
    help="Path to the file holding session state.",
)
def main(state: str):
    """A simple CLI for scraping Mercatorio data."""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level}</level> {message}",
        level="INFO",
        colorize=True,
    )

    if not os.environ.get("AIRTABLE_API_KEY"):
        logger.error("AIRTABLE_API_KEY environment variable is not set.")
        os.exit(1)

    logger.info("Initializing Airtable API client.")
    api = ApiClient(os.environ["AIRTABLE_API_KEY"])

    logger.info("Loading state from {}", state)
    scraper = Scraper(state)

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
        TownsMarketSync(BASE_NAME, scraper, api, whitelist),
    ]

    while True:
        for op in operations:
            logger.info("Running sync operation: {}", op.name)
            op.sync()

        now = datetime.datetime.now()
        seconds_until_next_hour = (60 - now.minute) * 60 - now.second
        seconds_to_sleep = seconds_until_next_hour + 60
        logger.info("Sleeping for {} seconds", seconds_to_sleep)
        time.sleep(seconds_to_sleep)


if __name__ == "__main__":
    main()
