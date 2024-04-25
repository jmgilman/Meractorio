import click

from loguru import logger
from mercatorio.scraper import Scraper

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

    logger.info("Loading cookies from {}", cookies)
    scraper = Scraper.from_cookies(cookies)


if __name__ == "__main__":
    main()
