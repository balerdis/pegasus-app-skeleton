from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService
from app.core.database.repositories.user_repository import UserRepository
from app.core.database.models.users import User
from pegasus_framework.auth.security.hash_password import PasswordHasher


class UserService(SqlAlchemyService):

    def create_user(self, data):
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            data.password = PasswordHasher().hash(data.password)
            user = repo.create(data.model_dump(), "email")
            uow.commit()
            user.password = None
            return user

    def get_user_by_id(self, user_id: int) -> User:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            return repo.get_by_id_or_fail(user_id)

    def get_user_by_email(self, email: str) -> User:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            return repo.get_by_email_or_fail(email)