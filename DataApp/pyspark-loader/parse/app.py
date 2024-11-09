import time
from random import randint

from fastapi import FastAPI, BackgroundTasks
from test_parse import debug_process_warc_file

DEBUG = True

app = FastAPI(debug=DEBUG)


@app.get('/debug-message')
async def debug_message():
    return {"debug": DEBUG, "status": "Parser server is running!"}


@app.get('/start-processing-warc')
async def start_processing(background_tasks: BackgroundTasks):
    background_tasks.add_task(debug_process_warc_file)
    return {"debug": DEBUG, "status": "start processing WARC files...", "etl_process_id": randint(1, 100)}


@app.get('/abort-warc-proccessing')
async def abort_processing():
    # TODO abort processing warc file with some kind of id
    meta_object = {}
    return {"debug": DEBUG, "status": "processed", "metadata": meta_object}
