import json

import bson
from fastapi import HTTPException, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pymongo.errors import PyMongoError

from api.settings import settings

from .rabbitmq_service import RabbitMQService


class MediaService:
    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.queue = RabbitMQService()

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

            file_id = str(file_id)

            message = json.dumps({
                'file_id': file_id,
            })

            await self.queue.publish(settings.VIDEO_QUEUE, message)

            return file_id
        except PyMongoError as e:
            print(e)
            HTTPException(status_code=500, detail='Error uploading file')
        except Exception as e:
            print(e)
            await gfs.delete(bson.ObjectId(file_id))
            HTTPException(status_code=500, detail='Error uploading file.')

    def download(self):
        return 'downloaded'
