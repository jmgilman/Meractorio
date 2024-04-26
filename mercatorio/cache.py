from typing import Iterable
import aiosqlite


class Cache:
    """A simple SQLite cache."""

    def __init__(self, path: str):
        self.db_path = path
        self.db = None

    async def execute(self, query: str, *args) -> Iterable[aiosqlite.Row]:
        """Execute a query."""
        async with self.db.execute(query, args) as cursor:
            return await cursor.fetchall()

    async def init(self):
        """Initialize the SQLite database connection."""
        self.db = await aiosqlite.connect(self.db_path)

    async def close(self):
        """Close the SQLite database."""
        await self.db.close()
