from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.db.db import close_db_connect, connect_and_init_db
from api.routers import health
from api.routers.auth import router as auth_router
from api.routers.media import router as media_router
from api.services.rabbitmq_service import RabbitMQService

rabbitmq_service = RabbitMQService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_and_init_db()
        await rabbitmq_service.connect()
        yield
    finally:
        await close_db_connect()
        await rabbitmq_service.close()

app = FastAPI(lifespan=lifespan)

app.include_router(health.router)
app.include_router(auth_router, prefix='/api/v1')
app.include_router(media_router, prefix='/api/v1')

@app.get('/')
def root():
    return {'version': '0.1.0'}
