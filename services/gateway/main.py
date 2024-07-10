from fastapi import FastAPI

from api.routers.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix='/api/v1')

@app.get('/')
def root():
    return {'version': '0.1.0'}
