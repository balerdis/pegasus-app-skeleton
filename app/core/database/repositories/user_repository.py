# app/core/database/repositories/user_repository.py
from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from app.core.database.models.users import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)