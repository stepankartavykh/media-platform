import asyncio
import os
import random
import threading
import time
from contextlib import asynccontextmanager
from inspect import trace

from sse_starlette.sse import EventSourceResponse
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request

from fastapi.openapi.utils import get_openapi

from database_storage_plugin import AsyncDatabaseStoragePlugin
from cache_plugin import AsyncCacheSystemPlugin
from connection_manager import ConnectionManager
# from content import generate_article_content, get_current_content
from dotenv import load_dotenv

load_dotenv()


connection_manager = ConnectionManager()
cache_system_plugin = AsyncCacheSystemPlugin()


class ContentEvent:
    pass


EVENT_UPDATE_STATE = False


def event_generator() -> None:
    global EVENT_UPDATE_STATE
    while True:
        time.sleep(random.randint(10, 20))
        EVENT_UPDATE_STATE = True


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    print(os.getenv('IS_CACHE_SERVICE_UPDATE_READY'))
    if os.getenv('IS_CACHE_SERVICE_UPDATE_READY') == 'True':
        cache_system_plugin.load_initial_data()
    thread = None
    if os.getenv('IS_LOCAL_DEV'):
        thread = threading.Thread(target=event_generator, args=())
        thread.start()
    yield
    print('Shutdown procedures...')
    if thread:
        thread.join(timeout=1.0)


app = FastAPI(debug=True, lifespan=lifespan)


@app.get("/change-frontend-state-signal")
async def accept_signal_to_change_frontend_state():
    # TODO endpoint to change frontend state. Requests are coming from other services(e.g. Dataflow/app).
    pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global EVENT_UPDATE_STATE
    await connection_manager.connect(websocket)
    # actual_content = await get_current_content(start_load=True)
    actual_content = {'debug_message': True, 'timestamp': time.time_ns()}
    await connection_manager.send_personal_message(str(actual_content), websocket)
    try:
        while True:
            if EVENT_UPDATE_STATE:
                # data_packet = await generate_article_content()
                data_packet = actual_content
                await connection_manager.broadcast(str(data_packet))
                print('broadcasting current state is complete!')
                EVENT_UPDATE_STATE = False
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f'websocket {websocket.client_state.value} closed!')


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
            if time.time() - _start > _TIMEOUT:
                break
            if await request.is_disconnected():
                print('request.is_disconnected == True')
                break
            message = new_messages()
            print(message)
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
