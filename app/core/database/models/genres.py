# app/core/database/models/genres.py
from sqlalchemy.orm import relationship
from app.core.database.models.base import Base
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime, 
    Boolean, 
    func, 
    Index
)

from pegasus_framework.db.models.mixins import AuditMixin

class Genre(AuditMixin, Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    movies = relationship("Movie", back_populates="genre")

    __table_args__ = (
        Index(
            "uq_genres_name_deleted_at",
            "name",
            "deleted_at",
            unique=True,
        ),        
        Index("ix_genres_active", "habilited", "deleted_at"),
        Index("ix_genres_name", "name"),
    )    