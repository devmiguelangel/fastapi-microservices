from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers.auth import router as auth_router
from api.routers.user import router as user_router

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router, prefix='/api/v1')
app.include_router(user_router, prefix='/api/v1')

@app.get('/')
def root():
    return {'service': 'auth', 'status': 'running'}
