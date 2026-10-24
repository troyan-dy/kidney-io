"""Publish the current time to the ``group`` topic exchange every second."""

import asyncio
import sys
import time

import aio_pika

AMQP_URL = "amqp://guest:guest@127.0.0.1/"
EXCHANGE_NAME = "group"
ROUTING_KEY = "pub.method.sub"
PUBLISH_INTERVAL = 1


async def main() -> None:
    """Connect to RabbitMQ and publish a timestamp message forever."""
    connection = await aio_pika.connect_robust(AMQP_URL)

    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
        )
        while True:
            text = f"cur time {time.time()}"
            await exchange.publish(
                aio_pika.Message(body=text.encode()),
                routing_key=ROUTING_KEY,
            )
            sys.stdout.write(f"{text}\n")
            await asyncio.sleep(PUBLISH_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
