from sqlalchemy.orm import Session

from api.models.users import User
from api.schemas.user_schema import UserCreateSchema
from api.utils.password import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreateSchema) -> User:
        data.password = hash_password(data.password)

        user = User(**data.model_dump())

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
