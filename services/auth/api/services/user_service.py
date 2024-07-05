from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api.repositories.user_repository import UserRepository
from api.schemas.user_schema import UserCreateSchema, UserOutputSchema


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_by_email(self, email: str) -> UserOutputSchema:
        user = self.repository.get_by_email(email)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        return UserOutputSchema(**user.__dict__)

    def create(self, data: UserCreateSchema) -> UserOutputSchema:
        try:
            user = self.repository.create(data)

            return UserOutputSchema(**user.__dict__)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
