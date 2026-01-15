# app/wiring/models/users.py
from pegasus_framework.auth.models.users.registry import register_user_model
from app.core.database.models.users import User

def register():
    register_user_model(User)

    return