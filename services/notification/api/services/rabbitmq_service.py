import asyncio

from aio_pika import Channel, Connection, IncomingMessage, connect

from api.services.notification_service import NotificationService
from api.settings import settings


class RabbitMQService:
    def __init__(self):
        self.amqp_url = f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
        self.connection: Connection = None
        self.channel: Channel = None
        self.consume_task: asyncio.Task = None
        self.notification_service = NotificationService()

    async def connect(self):
        if self.connection is None:
            self.connection = await connect(self.amqp_url)
            self.channel = await self.connection.channel()
            print('Connected to RabbitMQ')

    async def on_message(self, message: IncomingMessage) -> None:
        async with message.process():
            email_response = await self.notification_service.send_email(message.body)

            print('EMAIL#########################')
            print(email_response.json())
            print('#########################')

    async def consume(self, queue_name: str):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(self.on_message, no_ack=False)

    async def start_consume(self, queue_name: str):
        self.consume_task = asyncio.create_task(self.consume(queue_name))

    async def close(self):
        if self.consume_task:
            self.consume_task.cancel()
            try:
                await self.consume_task
            except asyncio.CancelledError:
                pass
            except Exception as unexpected_exception:
                print('Unexpected exception has occurred', unexpected_exception)
        if self.channel is not None:
            await self.channel.close()
            print('Closed channel to RabbitMQ')
        if self.connection is not None:
            await self.connection.close()
            print('Closed connection to RabbitMQ')
