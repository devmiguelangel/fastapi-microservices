from motor.motor_asyncio import AsyncIOMotorClient

from api.settings import settings

db_client: AsyncIOMotorClient = None

DB_URI = f'mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/?retryWrites=true&w=majority'

async def get_db() -> AsyncIOMotorClient:
    db_name = settings.DB_NAME

    return db_client[db_name]

async def connect_and_init_db():
    global db_client

    try:
        db_client = AsyncIOMotorClient(DB_URI,
            maxPoolSize=10,
            minPoolSize=3,
            uuidRepresentation='standard',
        )

        database = await get_db()

        try:
            ping_response = await database.command('ping')

            if int(ping_response['ok']) != 1:
                print('Problem connecting to database.')
            else:
                print('Connected to database.')
        except Exception as e:
            print(e)
    except Exception as e:
        print(f'Could not connect to database: {e}')
        raise

async def close_db_connect():
    global db_client

    if db_client is None:
        return
    db_client.close()
    db_client = None

    print('Closed connection to database.')
