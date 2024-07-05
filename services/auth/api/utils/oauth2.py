from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session

from api.models.database import get_db
from api.schemas.auth_schema import TokenDataSchema
from api.services.user_service import UserService
from api.settings import settings

SECRET_KEY = settings.jwt_secret
ALGORITHM = settings.jwt_algorithm
EXPIRES_IN = settings.jwt_expires_in

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRES_IN)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        'access_token': encoded_jwt,
        'token_type': 'bearer',
    }


def decode_access_token(token: str, credentials_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: EmailStr = payload.get('sub')

        if email is None:
            raise credentials_exception

        return TokenDataSchema(email=email)
    except JWTError as e:
        raise credentials_exception from e


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    token = decode_access_token(token, credentials_exception)

    user_service = UserService(session)
    user = user_service.get_by_email(token.email)

    if user is None:
        raise credentials_exception

    return user
