import asyncio
import multiprocessing
from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

from DataApp.dataflow.main import data_pipeline_simulation


@asynccontextmanager
async def lifespan(app_: FastAPI):
    print('Start app procedures...')
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=True, lifespan=lifespan)


def data_pipeline_from_api():
    asyncio.run(data_pipeline_simulation(count_times=4, interval=20))


def run_app():
    uvicorn.run(app, host="localhost", port=8000)


def main():
    app_process = multiprocessing.Process(target=run_app)
    app_process.start()

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=data_pipeline_from_api, trigger='interval', seconds=60, max_instances=1)
    scheduler.start()

    app_process.join()


if __name__ == "__main__":
    main()
