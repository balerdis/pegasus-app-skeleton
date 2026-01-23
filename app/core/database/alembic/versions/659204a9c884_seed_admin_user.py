"""seed admin user

Revision ID: 659204a9c884
Revises: 66f97015ad68
Create Date: 2026-01-23 19:32:58.969167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# revision identifiers, used by Alembic.
revision: str = '659204a9c884'
down_revision: Union[str, Sequence[str], None] = '66f97015ad68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    hashed_password = pwd_context.hash("12345678")

    conn = op.get_bind()

    # chequeo idempotente
    result = conn.execute(
        sa.text(
            """
            SELECT id FROM users
            WHERE email = :email
            """
        ),
        {"email": "admin@admin.com.ar"},
    ).fetchone()

    if result is None:
        conn.execute(
            sa.text(
                """
                INSERT INTO users (
                    email,
                    password,
                    created_at
                ) VALUES (
                    :email,
                    :password,
                    NOW()
                )
                """
            ),
            {
                "email": "admin@admin.com.ar",
                "password": hashed_password,
            },
        )


def downgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        sa.text(
            """
            DELETE FROM users
            WHERE email = :email
            """
        ),
        {"email": "admin@admin.com.ar"},
    )