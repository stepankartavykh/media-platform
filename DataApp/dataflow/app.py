import asyncio
import multiprocessing
import random
import time
from contextlib import asynccontextmanager
from typing import TypeAlias

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from DataApp.dataflow.html_page import html, html_multiple_connections
from DataApp.dataflow.main import data_pipeline_simulation


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get():
    return HTMLResponse(html_multiple_connections)


GeneratedArticleContent: TypeAlias = dict[str, str]


def generate_article_content() -> GeneratedArticleContent:
    number = random.randint(1, 1000)
    return {
        "number": f"{number}",
        "text": f"text info {number}",
        "qwe": 123
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            for i in range(3):
                await websocket.send_text(str(generate_article_content()))
                time.sleep(1)
            data = await websocket.receive_text()
            print("=" * 30, "DEBUG:", data)
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        # await websocket.close()
        print(f'websocket {websocket.client_state.value} closed!')


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


def data_pipeline_from_api():
    print("Processing data pipeline ...")
    # done = 10
    # for i in range(done + 1):
    #     print(f'Data pipeline working in progress({i / done * 100}%)...', )
    #     time.sleep(10)
    # asyncio.run(data_pipeline_simulation(count_times=4, interval=20))


def run_app():
    uvicorn.run(app, host="localhost", port=8000)


@app.get('/stop-data-pipeline')
async def stop_processing():
    pass


@app.get('/restart-loading')
async def restart_processing():
    pass


def app_with_data_pipeline():
    app_process = multiprocessing.Process(target=run_app)
    app_process.start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=data_pipeline_from_api, trigger='interval', seconds=5, max_instances=2)
    scheduler.start()

    app_process.join()


def simple_app():
    run_app()


if __name__ == "__main__":
    simple_app()
