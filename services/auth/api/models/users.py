from sqlalchemy import TIMESTAMP, UUID, Column, String, text
from uuid6 import uuid7

from api.models.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid7)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('NOW()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('NOW()'), onupdate=text('NOW()'))
