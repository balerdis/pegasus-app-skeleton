from app.core.services.base_service import BaseService
from pegasus_framework.core.security.hash_password import hash_password
from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.api.v1.schemas.users.responses import UserResponse
from app.core.database.repositories.user_repository import UserRepository


class UserService(BaseService):

    def create_user(self, data):
        with SqlAlchemyUnitOfWork() as uow:
            repo = uow.repo(UserRepository)
            data.password = hash_password(data.password)
            user.password = None
            user = repo.create(data.model_dump(), "email")
            uow.commit()
            return UserResponse(user.model_dump())