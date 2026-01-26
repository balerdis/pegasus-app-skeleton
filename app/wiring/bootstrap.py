# app/wiring/bootstrap.py

from fastapi import FastAPI
from app.wiring.models.users import register_user_model
from app.core.database.models.users import User
from pegasus_framework.db.unit_of_work.sqlalchemy_uow import SqlAlchemyUnitOfWork
from app.wiring.repositories.session_repository import REPOSITORY_BINDINGS

def bootstrap_application(app: FastAPI) -> None:
    """
    Punto único de configuración de la aplicación.
    """
    # 1. Registrar modelos concretos en el framework
    register_user_model(User)

    # 2. Registrar overrides de servicios

    # 3. Registrar middlewares

    # 4. Registrar repositories
    for abstraction, implementation in REPOSITORY_BINDINGS.items():
        SqlAlchemyUnitOfWork.bind_repository(
            abstraction,
            implementation,
        )    