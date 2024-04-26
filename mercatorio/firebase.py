import json
import time

from httpx import AsyncClient
from requests import Session


API_KEY = "AIzaSyAOEF0TZjQWE54ANjk-EttcCA2hm7IHglc"


class FirebaseAuthenticator:
    """Handles Firebase authentication."""

    def __init__(self, state_path: str):
        self.state_path = state_path
        self._load_state()

    async def refresh(self, session: AsyncClient):
        """Refresh the Firebase token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }
        response = await session.post(
            f"https://securetoken.googleapis.com/v1/token?key={API_KEY}",
            data=data,
        )
        auth_details = response.json()

        self.id_token = auth_details["id_token"]
        self.refresh_token = auth_details["refresh_token"]
        self.current_time = time.time()
        self.expires_in = auth_details["expires_in"]

        self._save_state()

    def _load_state(self):
        """Load the authentication state from a file.

        Args:
            path (str): The path to the file to load the state from.
        """
        with open(self.state_path, "r") as f:
            state = json.load(f)
            self.id_token = state["id_token"]
            self.refresh_token = state["refresh_token"]
            self.current_time = state["current_time"]
            self.expires_in = state["expires_in"]

    def _save_state(self):
        """Save the authentication state to a file.

        Args:
            path (str): The path to the file to save the state to.
        """
        state = {
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "current_time": self.current_time,
            "expires_in": self.expires_in,
        }
        with open(self.state_path, "w") as f:
            json.dump(state, f)
