import json

from aio_pika import Channel, Connection, Message, connect

from api.settings import settings


class RabbitMQService:
    def __init__(self):
        self.amqp_url = f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
        self.connection: Connection = None
        self.channel: Channel = None


    async def connect(self):
        if self.connection is None:
            self.connection = await connect(self.amqp_url)
            self.channel = await self.connection.channel()
            print('Connected to RabbitMQ')

    async def publish(self, queue_name: str, message: json):
        await self.connect()
        # `queue = await self.channel.declare_queue(queue_name, durable=True)` is creating a queue with the specified
        # `queue_name` on the RabbitMQ server using the current channel. The `durable=True` parameter indicates that the
        # queue should be durable, meaning it will survive a broker restart. The method returns a reference to the
        # declared queue, which is stored in the `queue` variable for further use.
        queue = await self.channel.declare_queue(queue_name, durable=True)

        # This line of code is publishing a message to a specific queue in RabbitMQ using the default exchange. Here's a
        # breakdown of what each part does:
        # - `await self.channel.default_exchange.publish` is publishing a message to the default exchange using the current
        # channel.
        # - `Message(body=message.encode())` is creating a message object with the message body set to the encoded JSON
        # string.
        # - `routing_key=queue.name` is specifying the routing key for the message, which is set to the name of the queue
        await self.channel.default_exchange.publish(
            Message(
                body=message.encode(),
            ),
            routing_key=queue.name,
        )

    async def close(self):
        if self.channel is not None:
            await self.channel.close()
            print('Closed channel to RabbitMQ')
        if self.connection is not None:
            await self.connection.close()
            print('Closed connection to RabbitMQ')
