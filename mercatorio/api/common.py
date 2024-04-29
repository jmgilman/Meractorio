from pydantic import BaseModel


class Location(BaseModel):
    """Represents the location of something on the map."""

    x: int
    y: int
