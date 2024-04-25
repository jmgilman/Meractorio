import json

import requests


class Scraper:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def from_cookies(path: str):
        """Create a new Scraper instance from a cookies file.

        The cookies file should be a JSON file containing an array of objects
        with the following keys:
            - name (str): The name of the cookie
            - value (str): The value of the cookie

        Args:
            path (str): Path to the cookies file

        Returns:
            Scraper: A new Scraper instance with the cookies set
        """
        scraper = Scraper()
        with open(path, "r") as f:
            cookies = json.load(f)
            for cookie in cookies:
                scraper.session.cookies.set(cookie["name"], cookie["value"])

        return scraper
