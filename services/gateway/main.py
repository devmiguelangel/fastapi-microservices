from fastapi import FastAPI

from api.db.db import close_db_connect, connect_and_init_db
from api.routers import health
from api.routers.auth import router as auth_router
from api.routers.media import router as media_router

app = FastAPI()

app.add_event_handler('startup', connect_and_init_db)
app.add_event_handler('shutdown', close_db_connect)

app.include_router(health.router)
app.include_router(auth_router, prefix='/api/v1')
app.include_router(media_router, prefix='/api/v1')

@app.get('/')
def root():
    return {'version': '0.1.0'}
