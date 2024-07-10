from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.services.auth_service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

security = HTTPBasic()

@router.post('/login')
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    _service = AuthService()
    token, err = await _service.login(credentials)

    if err:
        return err

    return token
