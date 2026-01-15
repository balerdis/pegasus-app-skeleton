from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from app.core.database.models.genres import Genre
from sqlalchemy.exc import IntegrityError
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError




class GenreRepository(BaseRepository[Genre]):
    def __init__(self, session: Session):
        super().__init__(Genre, session)

    def create(self, data: dict) -> Genre:
        try:
            return super().create(data)

        except IntegrityError as e:
            self.session.rollback()

            if "duplicate entry" in str(e.orig).lower():
                raise DuplicateEntityError(
                    entity="Genre",
                    field="name",
                    value=data.get("name"),
                ) from e

            raise