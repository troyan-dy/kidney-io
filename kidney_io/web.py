import asyncio
import json

import aioredis
import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI()


async def process_messages(ws: WebSocket, room_id):
    async def income_message():
        while True:
            data = await ws.receive()
            print(f"GOT {data}")

    redis = await aioredis.create_redis("redis://localhost")

    async def incode_event():
        res = await redis.subscribe(room_id)
        ch = res[0]
        async for pack in ch.iter():
            pack: bytes
            print("GOT", pack)
            await ws.send_text(pack.decode())

    try:
        await asyncio.gather(income_message(), incode_event())
    except Exception as e:
        print("disconnect", repr(e))
    finally:
        redis.close()
        await redis.wait_closed()


@app.get("/send_event/{room_id}/{message_raw}")
async def root(message_raw: str, room_id: str):
    redis = await aioredis.create_redis("redis://localhost")
    await redis.publish(room_id, message_raw.encode())
    redis.close()
    await redis.wait_closed()
    return "OK"


@app.websocket("/ws/{room_id}")
async def get_event(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await process_messages(websocket, room_id)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
