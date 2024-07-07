from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from api.models.users import User
from api.schemas.user_schema import UserCreateSchema
from api.utils.password import hash_password, verify_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_credentials(self, credentials: OAuth2PasswordRequestForm) -> User:
        user = self.db.query(User).filter(User.email == credentials.username).first()

        if not user or not verify_password(credentials.password, user.password):
            return None

        return user

    def get_by_email(self, email: EmailStr) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, data: UserCreateSchema) -> User:
        data.password = hash_password(data.password)

        user = User(**data.model_dump())

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
