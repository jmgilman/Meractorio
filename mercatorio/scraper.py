import json

import requests

from loguru import logger

from mercatorio.firebase import FirebaseAuthenticator


class Scraper:
    """A simple web scraper for Mercatorio."""

    auth: FirebaseAuthenticator
    session: requests.Session

    def __init__(self, state_path: str):
        self.session = requests.Session()
        self.auth = FirebaseAuthenticator(state_path)
        self.session.cookies.set("FIREBASE_ID_TOKEN", self.auth.id_token)

    def get(self, url: str, **kwargs):
        """Make a GET request to the given URL.

        Args:
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to requests.Session.get.

        Returns:
            requests.Response: The response from the server.
        """
        response = self.session.get(url, **kwargs)
        if response.status_code == 401:
            logger.info("Refreshing Firebase token")
            self.auth.refresh(self.session)
            self.session.cookies.set("FIREBASE_ID_TOKEN", self.auth.id_token)
            response = self.session.get(url, **kwargs)

        return self.session.get(url, **kwargs)
