from .movies import Movie
from .genres import Genre
from pegasus_framework.db.models.base import Base
__all__ = [
    "Movie",
    "Base",
    "Genre"
]