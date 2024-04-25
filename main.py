import click

from loguru import logger
from mercatorio.airtable.client import ApiClient
from mercatorio.api import map, towns
from mercatorio.scraper import Scraper

import os
import sys


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
    base = api.base_by_name("Raw Data")

    logger.info("Loading cookies from {}", cookies)
    scraper = Scraper.from_cookies(cookies)
    map_api = map.Map(scraper)
    towns_api = towns.Towns(scraper)

    logger.info("Updating regions table.")
    regions_table = api.table_by_name(base, "Regions")

    region_data = []
    for region in map_api.all():
        region_data.append(
            {
                "id": region.id,
                "name": region.name,
                "center_x": region.center.x,
                "center_y": region.center.y,
                "size": region.size,
            }
        )
    api.upsert_records_by_field(regions_table, "id", region_data)

    logger.info("Updating towns table.")
    towns_table = api.table_by_name(base, "Towns")

    town_data = []
    for town in towns_api.all():
        town_data.append(
            {
                "id": town.id,
                "name": town.name,
                "location_x": town.location.x,
                "location_y": town.location.y,
                "region": town.region,
                "capital": town.capital,
            }
        )
    api.upsert_records_by_field(towns_table, "id", town_data)


if __name__ == "__main__":
    main()
