import os
import subprocess
from random import randint
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from test_parse import run_tasks_with_multiprocessing_pool
import requests
import gzip

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
    not_loaded_files = []
    path_to_load_dump = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_paths_files'
    for crawl in crawl_names:
        response = requests.get(f'https://data.commoncrawl.org/crawl-data/{crawl}/warc.paths.gz')
        file_path = path_to_load_dump + '/' + crawl + '_warc.paths.gz'
        if response.status_code == 200:
            with open(file_path, 'wb') as response_writer:
                response_writer.write(response.content)
            with gzip.open(file_path, 'rb') as gz_opener:
                with open(path_to_load_dump + '/' + crawl + '_warc.paths', 'wb') as paths_writer:
                    paths_writer.write(gz_opener.read())
        else:
            not_loaded_files.append(crawl)

    return {"debug": DEBUG, 'not_loaded_files': not_loaded_files}


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
