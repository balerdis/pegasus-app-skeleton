from pegasus_framework.db.repositories.base_repository import BaseRepository
from .genre_repository import GenreRepository
from .movie_repository import MovieRepository

__all__ = ["BaseRepository", "GenreRepository", "MovieRepository"]