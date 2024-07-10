from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.models.database import get_db
from api.models.users import User
from api.schemas.auth_schema import TokenSchema
from api.services.auth_service import AuthService
from api.utils.oauth2 import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

@router.post('/login')
def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db)
) -> TokenSchema:
    _service = AuthService(session)

    return _service.get_access_token(credentials)

@router.get('/validate')
def me(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {'user': current_user}
