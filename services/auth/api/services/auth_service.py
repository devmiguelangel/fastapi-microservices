from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.repositories.user_repository import UserRepository
from api.utils.oauth2 import create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def get_access_token(self, credentials: OAuth2PasswordRequestForm) -> dict:
        user = self.user_repo.get_by_credentials(credentials)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid credentials')

        return create_access_token({'sub': user.email})
