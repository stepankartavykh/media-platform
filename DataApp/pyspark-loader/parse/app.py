import functools
from enum import StrEnum
import inspect
import os
from random import randint
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from data_loader import read_paths_file_and_download_dumps
from test_parse import run_tasks_with_multiprocessing_pool
import requests
import gzip

from dotenv import load_dotenv

load_dotenv()

LOCAL_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DEBUG = os.getenv('DEBUG') == 'True'
IS_CONTAINER = os.getenv('IS_CONTAINER') == 'False'
WARC_PATHS_DIR = \
    os.getenv('WARC_PATHS_DIR') if IS_CONTAINER else LOCAL_DIR + '/storage/warc_paths_dir'
WARC_PATHS_DIR_PROCESSED = \
    os.getenv('WARC_PATHS_DIR_PROCESSED') if IS_CONTAINER else LOCAL_DIR + '/storage/warc_paths_dir_processed'
WARC_FILES_DIR = \
    os.getenv('WARC_FILES_DIR') if IS_CONTAINER else LOCAL_DIR + '/storage/warc_files_dir'
WARC_FILES_DIR_PROCESSED = \
    os.getenv('WARC_FILES_DIR_PROCESSED') if IS_CONTAINER else LOCAL_DIR + '/storage/warc_files_dir_processed'


@asynccontextmanager
async def procedures_on_startup(app_: FastAPI):
    print('Start app procedures...')
    if not os.path.exists(WARC_PATHS_DIR):
        os.makedirs(WARC_PATHS_DIR)
    if not os.path.exists(WARC_PATHS_DIR_PROCESSED):
        os.makedirs(WARC_PATHS_DIR_PROCESSED)
    if not os.path.exists(WARC_FILES_DIR):
        os.makedirs(WARC_FILES_DIR)
    if not os.path.exists(WARC_FILES_DIR_PROCESSED):
        os.makedirs(WARC_FILES_DIR_PROCESSED)
    yield
    print('Shutdown procedures...')


app = FastAPI(debug=DEBUG, lifespan=procedures_on_startup)


@app.get('/debug-message')
async def debug_message():
    return {"debug": DEBUG, "status": "Parser server is running!"}


@app.get('/load-all-warc-files')
async def load_all_warc_path_files(unzip_archive: bool = False, load_dump_count: int = 10):
    """Download files with paths for WARC files."""
    import os
    crawl_names = os.getenv('WARC_CRAWL_NAMES').split()
    not_loaded_files = []
    for crawl in crawl_names[:load_dump_count]:
        response = requests.get(f'https://data.commoncrawl.org/crawl-data/{crawl}/warc.paths.gz', verify=False)
        file_path = WARC_PATHS_DIR + '/' + crawl + '_warc.paths.gz'
        if response.status_code == 200:
            with open(file_path, 'wb') as response_writer:
                response_writer.write(response.content)
            if unzip_archive:
                with gzip.open(file_path, 'rb') as gz_opener:
                    with open(WARC_PATHS_DIR + '/' + crawl + '_warc.paths', 'wb') as paths_writer:
                        paths_writer.write(gz_opener.read())
                os.remove(file_path)
        else:
            not_loaded_files.append(crawl)
    return {"debug": DEBUG, 'not_loaded_files': not_loaded_files}


@app.get('/load-some-warc-files')
async def load_some_warc_files(paths_file_name: str, count_dumps: int):
    read_paths_file_and_download_dumps(WARC_PATHS_DIR + '/' + paths_file_name, WARC_FILES_DIR, count_dumps)
    return {"debug": DEBUG, "status": 'success'}


@app.post('/start-processing-warc')
async def start_processing(background_tasks: BackgroundTasks, file_names: list[str] = None):
    task = functools.partial(run_tasks_with_multiprocessing_pool, file_names=file_names)
    background_tasks.add_task(task)
    return {"debug": DEBUG, "status": "start processing WARC files...", "etl_process_id": randint(1, 100)}


@app.get('/abort-warc-proccessing')
async def abort_processing():
    # TODO abort processing warc file with some kind of id
    meta_object = {}
    return {"debug": DEBUG, "status": "processed", "metadata": meta_object}


class PossibleFileType(StrEnum):
    paths = 'paths'
    warc = 'warc'


@app.get('/get-unprocessed-warc-files')
async def get_unprocessed_files(file_type: PossibleFileType):
    return os.listdir(WARC_FILES_DIR)


PARSER_APP_HOST = 'localhost'
PARSER_APP_PORT = 7777


def run_app():
    uvicorn.run('app:app', host=PARSER_APP_HOST, port=PARSER_APP_PORT, reload=True)


if __name__ == "__main__":
    run_app()
