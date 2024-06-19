import asyncio
import multiprocessing
import os
import random
import time
from contextlib import asynccontextmanager
from typing import TypeAlias

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    app_.start_up_time = time.time()
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


def run_app():
    uvicorn.run(app, host="localhost", port=8000)


@app.get('/stop-data-pipeline')
async def stop_processing():
    pass


@app.get('/restart-loading')
async def restart_processing():
    pass


def background_task():
    while True:
        print(f'DEBUG UNDER PROCESS ({os.getpid()})', time.time())
        time.sleep(2)
        if time.time() - app.start_up_time > 15:
            multiprocessing.current_process().join()
            break


@app.get('/start-job')
def start_job():
    t2 = multiprocessing.Process(target=background_task)
    t2.start()
    return {"status": "Task is running."}


def simple_app():
    run_app()


if __name__ == "__main__":
    simple_app()
