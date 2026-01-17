# app/core/database/repositories/user_repository.py
from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from pegasus_framework.core.exceptions.domain.entity_not_found import EntityNotFoundError
from app.core.database.models.users import User
from typing import Optional

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        smt = self._base_query().where(User.email == email)
        return self.session.execute(smt).scalar_one_or_none()
    
    def get_by_email_or_fail(self, email: str) -> User:
        db_obj = self.get_by_email(id)
        if db_obj is None:
            raise EntityNotFoundError(f"{self.model_class.__name__} con email={email} no encontrado")
        return db_obj    