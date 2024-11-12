import asyncio
import os
import random
import time
from contextlib import asynccontextmanager
from sse_starlette.sse import EventSourceResponse
import uvicorn
from fastapi import FastAPI, Request

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


app = FastAPI(debug=True, lifespan=lifespan)


@app.get("/change-frontend-state-signal")
async def accept_signal_to_change_frontend_state():
    # TODO endpoint to change frontend state. Requests are coming from other services(e.g. Dataflow/app).
    pass


STREAM_DELAY = 0.2


class MessageInterface:
    @classmethod
    def build_message(cls):
        mess = {"timestamp": time.time_ns(), "test_number": random.randint(0, 1000)}
        return mess


@app.get('/stream')
async def message_stream(request: Request):
    print('start streaming...')

    _TIMEOUT = 5
    _start = time.time()

    def new_messages():
        for _ in range(10):
            yield MessageInterface.build_message()

    async def event_to_stream_generator():
        while True:
            if await request.is_disconnected() or time.time() - _start > _TIMEOUT:
                break
            message = new_messages()
            if message:
                yield message
            await asyncio.sleep(STREAM_DELAY)

    response = EventSourceResponse(event_to_stream_generator())
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


FRONTEND_APP_HOST = 'localhost'
FRONTEND_APP_PORT = 8001


storage_plugin = AsyncDatabaseStoragePlugin()


@app.get("/last-packets")
async def get_last_packets():
    packets = await storage_plugin.get_packets(100)
    api_data = [elem[0] for elem in packets]
    return api_data


def run_app():
    uvicorn.run('app:app', host=FRONTEND_APP_HOST, port=FRONTEND_APP_PORT, reload=True)


if __name__ == "__main__":
    run_app()
