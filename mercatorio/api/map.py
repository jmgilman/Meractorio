from pydantic import BaseModel, RootModel

from mercatorio.scraper import Scraper

BASE_URL = "https://play.mercatorio.io/api/map/regions"


class Center(BaseModel):
    """Represents the center of a region."""

    x: int
    y: int


class Region(BaseModel):
    """Represents a region in the game."""

    id: int
    name: str
    center: Center
    size: int


class RegionsList(RootModel):
    """Represents a list of regions in the game."""

    root: list[Region]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, position):
        return self.root[position]


class Map:
    """A class for interacting with the map API endpoint."""

    scraper: Scraper

    def __init__(self, scraper):
        self.scraper = scraper

    def all(self):
        """Get a list of all regions in the game.

        Returns:
            RegionsList: A list of all regions in the game
        """
        response = self.scraper.session.get(BASE_URL)
        return RegionsList.model_validate(response.json())
