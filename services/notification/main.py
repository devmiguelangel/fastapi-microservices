from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.services.rabbitmq_service import RabbitMQService
from api.settings import settings

rabbitmq_service = RabbitMQService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await rabbitmq_service.start_consume(settings.AUDIO_QUEUE)
        yield
    finally:
        await rabbitmq_service.close()

app = FastAPI(lifespan=lifespan)


@app.get('/')
def root():
    return {'version': '0.1.0'}
