import requests
import httpx

from loguru import logger

from mercatorio.firebase import FirebaseAuthenticator


class Scraper:
    """A simple web scraper for Mercatorio."""

    auth: FirebaseAuthenticator
    session: httpx.AsyncClient

    def __init__(self, state_path: str):
        self.session = requests.Session()
        self.session = httpx.AsyncClient(http2=True)
        self.auth = FirebaseAuthenticator(state_path)
        self.session.cookies.set("FIREBASE_ID_TOKEN", self.auth.id_token)

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Make a GET request to the given URL.

        Args:
            url (str): The URL to make the request to.
            **kwargs: Additional keyword arguments to pass to httpx.

        Returns:
            requests.Response: The response from the server.
        """
        response = await self.session.get(url, **kwargs)
        if response.status_code == 401:
            logger.info("Refreshing Firebase token")
            await self.auth.refresh(self.session)
            self.session.cookies.set("FIREBASE_ID_TOKEN", self.auth.id_token)
            response = await self.session.get(url, **kwargs)

        return response

    async def close(self):
        await self.session.aclose()
