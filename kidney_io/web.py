"""HTTP API of the service."""

import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


# WPS463: the endpoint is a stub that answers ``null``. Renaming ``get_event``
# would change ``summary`` and ``operationId`` in the OpenAPI schema.
# No docstring on purpose: FastAPI would publish it as the OpenAPI description.
@app.get("/analis/{analis_id}")
async def get_event(req: Request, analis_id: str) -> None:  # noqa: WPS463
    ...  # not implemented yet


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
