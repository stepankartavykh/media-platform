import gzip
import os
import subprocess

MAIN_URL = 'https://data.commoncrawl.org'
path_to_load_dump = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_dumps'


def _download_dumps(dump_name: str) -> None:
    command = ['wget', MAIN_URL + '/' + dump_name, '-P', path_to_load_dump]
    subprocess.run(command)


def read_paths_file_and_download_dumps(warc_paths_file: str, dumps_limit_count: int = None):
    already_loaded_files = os.listdir(path_to_load_dump)
    for loaded_warc_file_name in already_loaded_files:
        if not loaded_warc_file_name.endswith('.warc.gz'):
            raise Exception('Wrong file in directory that must contain only WARC files!')
    counter = 0
    with gzip.open(warc_paths_file, 'rt') as file_reader:
        for dump_part in file_reader:
            warc_file_name = dump_part.split('/')[-1].strip('\n')
            if warc_file_name in already_loaded_files:
                continue
            _download_dumps(dump_part.strip('\n'))
            counter += 1
            if dumps_limit_count and counter >= dumps_limit_count:
                break
