import os
from random import randint
import uvicorn
from fastapi import FastAPI, BackgroundTasks

from DataApp.dataloader.test_crawled_data_load import read_paths_file_and_download_dumps
from test_parse import run_tasks_with_multiprocessing_pool
import requests
import gzip

from dotenv import load_dotenv

DEBUG = True

app = FastAPI(debug=DEBUG)

load_dotenv()

WARC_PATHS_DIR = os.getenv('WARC_PATHS_DIR')
WARC_FILES_DIR = os.getenv('WARC_FILES_DIR')


@app.get('/debug-message')
async def debug_message():
    return {"debug": DEBUG, "status": "Parser server is running!"}


@app.get('/load-all-warc-files')
async def load_all_warc_path_files(unzip_archive: bool = False, load_dump_count: int = 10):
    import os
    crawl_names = os.getenv('WARC_CRAWL_NAMES').split()
    not_loaded_files = []
    for crawl in crawl_names[:load_dump_count]:
        response = requests.get(f'https://data.commoncrawl.org/crawl-data/{crawl}/warc.paths.gz')
        file_path = WARC_PATHS_DIR + '/' + crawl + '_warc.paths.gz'
        if response.status_code == 200:
            with open(file_path, 'wb') as response_writer:
                response_writer.write(response.content)
            if unzip_archive:
                with gzip.open(file_path, 'rb') as gz_opener:
                    with open(WARC_PATHS_DIR + '/' + crawl + '_warc.paths', 'wb') as paths_writer:
                        paths_writer.write(gz_opener.read())
        else:
            not_loaded_files.append(crawl)

    return {"debug": DEBUG, 'not_loaded_files': not_loaded_files}


@app.get('/load-some-warc-files')
async def load_some_warc_files(paths_file_name: str, count_dumps: int):
    read_paths_file_and_download_dumps(WARC_PATHS_DIR + '/' + paths_file_name, count_dumps,
                                       load_dumps_to_path=WARC_FILES_DIR)
    return {"debug": DEBUG, "status": 'success'}


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
