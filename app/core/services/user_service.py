# app/core/services/user_service.py
from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService
from pegasus_framework.core.security.hash_password import hash_password

from app.api.v1.schemas.users.responses import UserResponse
from app.core.database.repositories.user_repository import UserRepository


class UserService(SqlAlchemyService):

    def create_user(self, data):
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            data.password = hash_password(data.password)
            user.password = None
            user = repo.create(data.model_dump(), "email")
            uow.commit()
            return UserResponse(user.model_dump())