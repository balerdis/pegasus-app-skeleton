from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from app.core.database.models.genres import Genre





class GenreRepository(BaseRepository[Genre]):
    def __init__(self, session: Session):
        super().__init__(Genre, session)