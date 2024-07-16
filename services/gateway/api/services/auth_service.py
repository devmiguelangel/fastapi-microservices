import httpx
from fastapi import HTTPException, status
from fastapi.security import HTTPBasicCredentials

from api.settings import settings


class AuthService:
    async def login(self, credentials: HTTPBasicCredentials):
        async with httpx.AsyncClient() as client:
            data = {
                'username': credentials.username,
                'password': credentials.password,
            }

            response = await client.post(
                f'{settings.AUTH_URL}/auth/login',
                data=data,
            )

            if response.status_code == status.HTTP_200_OK:
                return response.json()

            raise HTTPException(status_code=response.status_code, detail=response.json())

    async def validate(self, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'{settings.AUTH_URL}/auth/validate',
                headers={
                    'Authorization': f'Bearer {token}'
                }
            )

            if response.status_code == status.HTTP_200_OK:
                return response.json()

            raise HTTPException(status_code=response.status_code, detail=response.json())
