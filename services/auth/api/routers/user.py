from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models.database import get_db
from api.schemas.user_schema import UserCreateSchema, UserOutputSchema
from api.services.user_service import UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.post('/')
def create_user(data: UserCreateSchema, session: Session = Depends(get_db)) -> UserOutputSchema:
    _service = UserService(session)
    return _service.create(data)
