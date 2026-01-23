from sqlalchemy.exc import IntegrityError
from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService
from app.core.database.repositories.user_repository import UserRepository
from app.core.database.models.users import User
from pegasus_framework.auth.security.hash_password import PasswordHasher
from app.api.v1.schemas.users.responses import UserResponse
from pegasus_framework.core.exceptions.domain import DuplicateEntityError
from app.core.services.dto.user.user_create_dto import UserUpdateDTO

class UserService(SqlAlchemyService):

    def get_all(self) -> list[UserResponse]:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            entities = repo.get_all()
            return [self._map_user_to_response(e) for e in entities]
        
    def create_user(self, data):
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            data.password = PasswordHasher().hash(data.password)
            try:
                user = repo.create(data.model_dump())
                uow.commit()
            except IntegrityError as exc:
                uow.rollback()
                if "uq_users_email" in str(exc.orig):
                    raise DuplicateEntityError(
                        entity="User",
                        field="email",
                        value=data.email,
                    ) from exc
                raise
            user.password = None
            return self._map_user_to_response(user)

    def get_user_by_id(self, user_id: int) -> User:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            return repo.get_by_id_or_fail(user_id)

    def get_user_by_email(self, email: str) -> User:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            return repo.get_by_email_or_fail(email)
        
    def get_by_id_or_fail(self, id: int) -> UserResponse:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            entity = repo.get_by_id_or_fail(id)
            return self._map_user_to_response(entity)           
        
    def update(self, id: int, data: UserUpdateDTO) -> UserResponse:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            entity = repo.get_by_id_or_fail(id)
            update_data = data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(entity, field, value)
                
            ## No hacer update, el genre ya esta atachado en la sesion y 
            ## el SqlAlchemy trackea los cambios en el objeto atachado automaticamente    
            # genre_updated = uow.genres.update(genre)
            ## El commit de la uow genera el flush automatico antes del commit
            uow.commit()
            return self._map_user_to_response(entity)

    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        with self._uow() as uow:
            repo = uow.repo(UserRepository)
            if confirm: 
                repo.delete_by_id(id, confirm)
                uow.commit()

    def _map_user_to_response(self, m) -> UserResponse:
        return UserResponse(
            id=m.id,
            email=m.email,
            name=m.name,
            habilited=m.habilited
        )
    
 