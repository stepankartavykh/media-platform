import gzip
import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

path_to_load_dump = os.getenv('PATH_TO_LOAD_DUMP')


MAIN_URL = 'https://data.commoncrawl.org'


def _download_dump(dump_name: str) -> None:
    command = ['wget', '--no-check-certificate', MAIN_URL + '/' + dump_name, '-P', path_to_load_dump]
    subprocess.run(command)


def read_paths_file_and_download_dumps(warc_paths_file: str, dumps_limit_count: int = None,
                                       load_dumps_to_path: str = path_to_load_dump,
                                       use_multiple_processes: bool = True, count_processes: int = 1):
    already_loaded_files = os.listdir(load_dumps_to_path)
    # TODO some flaws with logic in containers. Check it out!
    # for loaded_warc_file_name in already_loaded_files:
    #     if not loaded_warc_file_name.endswith('.warc.paths'):
    #         raise Exception(f'Wrong file in directory {load_dumps_to_path} that must contain only WARC files!')
    counter = 0
    with gzip.open(warc_paths_file, 'rt') as file_reader:
        for dump_part in file_reader:
            warc_file_name = dump_part.split('/')[-1].strip('\n')
            if warc_file_name in already_loaded_files:
                continue
            _download_dump(dump_part.strip('\n'))
            counter += 1
            if dumps_limit_count and counter >= dumps_limit_count:
                break
