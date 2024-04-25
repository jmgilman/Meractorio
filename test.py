from mercatorio.api import map, towns
from mercatorio.scraper import Scraper

scraper = Scraper.from_cookies("cookies.json")

map = map.Map(scraper)
towns = towns.Towns(scraper)
