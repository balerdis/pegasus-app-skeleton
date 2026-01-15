# app/wiring/bootstrap.py

from fastapi import FastAPI
from pegasus_framework.wiring.bootstrap import get_user_service
from app.overrides.users import get_user_service_override
from app.wiring.models.users import register_user_model
from app.core.database.models.users import User

def bootstrap_application(app: FastAPI) -> None:
    """
    Punto único de configuración de la aplicación.
    """
    # 1. Registrar modelos concretos en el framework
    register_user_model(User)

    # 2. Registrar overrides de servicios
    app.dependency_overrides[get_user_service] = get_user_service_override
