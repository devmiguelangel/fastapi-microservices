from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from motor.motor_asyncio import AsyncIOMotorClient

from api.db.db import get_db
from api.services.auth_service import AuthService
from api.services.media_service import MediaService

router = APIRouter(
    prefix='/media',
    tags=['media']
)

security = HTTPBearer()

@router.post('/upload')
async def upload(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], file: UploadFile, db: AsyncIOMotorClient = Depends(get_db)):
    auth_service = AuthService()
    media_service = MediaService(db)

    user = await auth_service.validate(credentials.credentials)
    video_fid = await media_service.upload(file, user)
    audio_fid = None

    message = {
        'video_fid': video_fid,
        'audio_fid': audio_fid,
        'user': user.get('email'),
    }

    return message

@router.get('/download')
def download():
    media_service = MediaService()
    res = media_service.download()

    return {'message': 'downloaded'}
