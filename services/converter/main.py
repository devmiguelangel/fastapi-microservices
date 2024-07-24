from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.db.db import close_db_connect, connect_and_init_db
from api.services.rabbitmq_service import RabbitMQService
from api.settings import settings

rabbitmq_service = RabbitMQService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_and_init_db()
        await rabbitmq_service.start_consume(settings.VIDEO_QUEUE)
        yield
    finally:
        await close_db_connect()
        await rabbitmq_service.close()

app = FastAPI(lifespan=lifespan)


@app.get('/')
def root():
    return {'version': '0.1.0'}
