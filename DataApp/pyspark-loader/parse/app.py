import os
import subprocess
from random import randint
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from test_parse import run_tasks_with_multiprocessing_pool

from dotenv import load_dotenv

DEBUG = True

app = FastAPI(debug=DEBUG)


WARC_PATHS_DIR = os.getenv('WARC_PATHS_DIR')


@app.get('/debug-message')
async def debug_message():
    return {"debug": DEBUG, "status": "Parser server is running!"}


@app.get('/load-all-warc-files')
async def load_all_warc_path_files():
    import os
    crawl_names = os.getenv('WARC_CRAWL_NAMES').split()
    path_to_load_dump = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_dumps'
    for crawl in crawl_names[:5]:
        command = ['wget', f'https://data.commoncrawl.org/crawl-data/{crawl}/warc.paths.gz', '-P',
                   path_to_load_dump, '-O', crawl + 'warc.paths.gz']
        subprocess.run(command)


@app.get('/start-processing-warc')
async def start_processing(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_tasks_with_multiprocessing_pool)
    return {"debug": DEBUG, "status": "start processing WARC files...", "etl_process_id": randint(1, 100)}


@app.get('/abort-warc-proccessing')
async def abort_processing():
    # TODO abort processing warc file with some kind of id
    meta_object = {}
    return {"debug": DEBUG, "status": "processed", "metadata": meta_object}


PARSER_APP_HOST = 'localhost'
PARSER_APP_PORT = 8002


def run_app():
    uvicorn.run('app:app', host=PARSER_APP_HOST, port=PARSER_APP_PORT, reload=True)


if __name__ == "__main__":
    run_app()
