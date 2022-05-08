import asyncio
import time

import aio_pika
from aio_pika import exchange


async def main(loop):
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)

    async with connection:
        routing_key = "pub.method.sub"
        exchange_name = "group"
        channel = await connection.channel()
        logs_exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)
        while 1:
            _message = f"cur time {time.time()}"
            message = aio_pika.Message(body=_message.encode())
            await logs_exchange.publish(message, routing_key=routing_key)
            print(_message)
            await asyncio.sleep(1)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
