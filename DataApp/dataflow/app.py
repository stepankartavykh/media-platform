import multiprocessing
import os
import random
import time
from contextlib import asynccontextmanager
from enum import Enum
from typing import TypeAlias

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from DataApp.dataflow.main import data_pipeline_simulation

START_UP_TIME = time.time()


def load_available_dumps():
    # TODO create loader for dumps in storage.
    pass


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    loader_process = multiprocessing.Process(target=load_available_dumps)
    loader_process.start()
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan)

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
            await websocket.send_text(str(generate_article_content()))
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print(f'websocket {websocket.client_state.value} closed!')


@app.get('/stop-data-pipeline')
async def stop_processing():
    pass


@app.get('/restart-loading')
async def restart_processing():
    pass


class ContentStatus(Enum):
    pass


@app.get('/content-status')
def get_content_status():
    return {
        'status': 'full'
    }


@app.get('/run-pipeline/{query}')
async def run_pipeline(query: str):
    await data_pipeline_simulation(query)
    return {"status": f"pipeline for query = {query} is completed!"}


def run_app():
    uvicorn.run('DataApp.dataflow.app:app', host="localhost", port=7999, workers=4)


if __name__ == "__main__":
    run_app()
