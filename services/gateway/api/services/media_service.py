from fastapi import HTTPException, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo.errors import PyMongoError


class MediaService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db

    async def upload(self, file: UploadFile, user: dict) -> str:
        try:
            gfs = AsyncIOMotorGridFSBucket(self.db, bucket_name='videos')
            file_id = await gfs.upload_from_stream(
                file.filename,
                file.file,
                metadata={
                    'uploader': user,
                }
            )

            return str(file_id)
        except PyMongoError as e:
            print(e)
            HTTPException(status_code=500, detail='Error uploading file')

    def download(self):
        return 'downloaded'
