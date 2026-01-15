# app/wiring/bootstrap.py

from fastapi import FastAPI
from app.wiring.models.users import register_user_model
from app.core.database.models.users import User

def bootstrap_application(app: FastAPI) -> None:
    """
    Punto único de configuración de la aplicación.
    """
    # 1. Registrar modelos concretos en el framework
    register_user_model(User)

    # 2. Registrar overrides de servicios

    # 3. Registrar middlewares