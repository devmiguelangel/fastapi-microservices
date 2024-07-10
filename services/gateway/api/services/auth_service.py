import httpx
from fastapi import status
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
                return response.text, None

            return None, (response.text, response.status_code)
