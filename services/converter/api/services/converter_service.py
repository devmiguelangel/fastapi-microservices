import json
import tempfile

import moviepy.editor
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from api.db.db import get_db
from api.settings import settings


class ConverterService:
    async def get_db(self) -> AsyncIOMotorClient:
        return await get_db()

    async def to_mp3(self, message: json, publish: callable) -> str:
        try:
            db: AsyncIOMotorClient = await self.get_db()
            self.fs_videos = AsyncIOMotorGridFSBucket(db, bucket_name='videos')
            self.fs_audios = AsyncIOMotorGridFSBucket(db, bucket_name='audios')

            message = json.loads(message)
            file_id = message['file_id']

            video_data = await self.download_video(file_id)
            audio_id = await self.convert_and_upload_audio(video_data, file_id)

            if audio_id is not None:
                await publish(settings.AUDIO_QUEUE, json.dumps({'audio_id': audio_id}))

            return audio_id
        except Exception as e:
            print(e)
            return None

    async def download_video(self, file_id: str) -> bytes:
        video = await self.fs_videos.open_download_stream(ObjectId(file_id))
        video_data = await video.read()

        return video_data

    async def convert_and_upload_audio(self, video_data: bytes, file_id: str):
        with tempfile.NamedTemporaryFile() as temp_video, \
                tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
            temp_video.write(video_data)
            temp_video.flush()

            audio = moviepy.editor.VideoFileClip(temp_video.name).audio
            audio_file_name = f'{file_id}.mp3'
            audio.write_audiofile(temp_audio.name)

            with open(temp_audio.name, 'rb') as data:
                audio_id = await self.fs_audios.upload_from_stream(
                    audio_file_name,
                    data,
                    metadata={
                        'uploader': 'converter'
                    }
                )

        return str(audio_id)
