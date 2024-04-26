from mercatorio.api import map, towns
from mercatorio.scraper import Scraper

scraper = Scraper("state.json")

map = map.Map(scraper)
towns = towns.Towns(scraper)
