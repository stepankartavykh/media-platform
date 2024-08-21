import asyncio
import os
import random
import threading
import time
from contextlib import asynccontextmanager
from sse_starlette.sse import EventSourceResponse
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request

from FrontendApp.app.cache_plugin import AsyncCacheSystemPlugin
from FrontendApp.app.connection_manager import ConnectionManager
from FrontendApp.app.content import generate_article_content, get_current_content
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
    if os.getenv('IS_CACHE_SERVICE_UPDATE_READY'):
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
    actual_content = await get_current_content(start_load=True)
    await connection_manager.send_personal_message(actual_content.convert_data(), websocket)
    try:
        while True:
            if EVENT_UPDATE_STATE:
                data_packet = await generate_article_content()
                await connection_manager.broadcast(data_packet.json())
                print('broadcasting current state is complete!')
                EVENT_UPDATE_STATE = False
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        print(f'websocket {websocket.client_state.value} closed!')


STREAM_DELAY = 1
RETRY_TIMEOUT = 15000


class MessageInterface:
    @classmethod
    def build_message(cls):
        pass


@app.get('/stream')
async def message_stream(request: Request):
    def new_messages():
        for _ in range(100):
            yield MessageInterface.build_message()

    async def event_to_stream_generator():
        while True:
            if await request.is_disconnected():
                break
            message = new_messages()
            if message:
                yield message
            await asyncio.sleep(STREAM_DELAY)
    return EventSourceResponse(event_to_stream_generator())


FRONTEND_APP_HOST = 'localhost'
FRONTEND_APP_PORT = 8001


def run_app():
    uvicorn.run('FrontendApp.app:app', host=FRONTEND_APP_HOST, port=FRONTEND_APP_PORT)


if __name__ == "__main__":
    run_app()
