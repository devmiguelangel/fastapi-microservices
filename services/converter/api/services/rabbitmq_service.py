import asyncio
import json

from aio_pika import Channel, Connection, IncomingMessage, Message, connect

from api.services.converter_service import ConverterService
from api.settings import settings


class RabbitMQService:
    def __init__(self):
        self.amqp_url = f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
        self.connection: Connection = None
        self.channel: Channel = None
        self.consume_task: asyncio.Task = None
        self.converter_service = ConverterService()

    async def connect(self):
        if self.connection is None:
            self.connection = await connect(self.amqp_url)
            self.channel = await self.connection.channel()
            print('Connected to RabbitMQ')

    async def publish(self, queue_name: str, message: json):
        await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=True)

        await self.channel.default_exchange.publish(
            Message(
                body=message.encode(),
            ),
            routing_key=queue.name,
        )

    async def on_message(self, message: IncomingMessage) -> None:
        async with message.process():
            audio_id = await self.converter_service.to_mp3(message.body, self.publish)

            if audio_id is not None:
                print(f'Audio ID {audio_id} has been created')

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
