import asyncio

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/analis/{analis_id}")
async def get_event(req: Request, analis_id: str):
    pass


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
