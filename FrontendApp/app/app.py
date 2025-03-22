import asyncio
import logging
import random
import time
from contextlib import asynccontextmanager
from typing import Iterable

from sse_starlette.sse import EventSourceResponse
import uvicorn
from fastapi import FastAPI, Request, HTTPException

from database_storage_plugin import AsyncDatabaseStoragePlugin
from cache_plugin import AsyncCacheSystemPlugin
from connection_manager import ConnectionManager
from dotenv import load_dotenv

load_dotenv()

connection_manager = ConnectionManager()
cache_system_plugin = AsyncCacheSystemPlugin()

EVENT_UPDATE_STATE = False


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan, log_level="trace")


@app.get("/change-frontend-state-signal")
async def accept_signal_to_change_frontend_state():
    # TODO endpoint to change frontend state. Requests are coming from other services(e.g. Dataflow/app).
    pass


STREAM_DELAY = 0.2


class MessageInterface:
    @classmethod
    def build_messages(cls) -> Iterable:
        return [
            {
                "timestamp": time.time_ns(),
                "test_number": random.randint(0, 1000)
            }
        ]


async def event_generator(request: Request, start_time: float, timeout: float, stream_delay: float):
    while True:
        if await request.is_disconnected() or time.time() - start_time > timeout:
            break
        for message in MessageInterface.build_messages():
            yield message
        await asyncio.sleep(stream_delay)


@app.get('/stream')
async def message_stream(request: Request):
    logging.info('start streaming...')

    _TIMEOUT = 5
    _start = time.time()

    response = EventSourceResponse(event_generator(request, _start, _TIMEOUT, STREAM_DELAY))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


FRONTEND_APP_HOST = 'localhost'
FRONTEND_APP_PORT = 8001

storage_plugin = AsyncDatabaseStoragePlugin()


@app.get("/last-packets")
async def get_last_packets(count: int = 100):
    if count < 1:
        raise HTTPException(status_code=400,
                            detail='count must be greater than 0.')
    return await storage_plugin.get_packets(count)


def run_app():
    uvicorn.run('app:app', host=FRONTEND_APP_HOST, port=FRONTEND_APP_PORT, reload=True)


if __name__ == "__main__":
    run_app()
