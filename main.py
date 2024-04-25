import click

from loguru import logger
from mercatorio.airtable.client import ApiClient
from mercatorio.airtable.operations import RegionsSync, TownsSync
from mercatorio.api import map, towns
from mercatorio.scraper import Scraper

import os
import sys

BASE_NAME = "Raw Data"


@click.command()
@click.option(
    "--cookies",
    type=click.Path(exists=True),
    default="cookies.json",
    help="Path to the file holding Mercatorio cookies.",
)
def main(cookies):
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

    logger.info("Loading cookies from {}", cookies)
    scraper = Scraper.from_cookies(cookies)

    # Define the operations to run.
    # Comment out any operations you don't want to run.
    operations = [
        RegionsSync(BASE_NAME, scraper, api),
        TownsSync(BASE_NAME, scraper, api),
    ]

    for op in operations:
        logger.info("Running sync operation: {}", op.name)
        op.sync()


if __name__ == "__main__":
    main()
