import _io
import gzip
import subprocess
import time
from collections import defaultdict

from warcio.archiveiterator import ArchiveIterator
from warcio.recordloader import ArcWarcRecord

crawled_data_packet = 'CC-MAIN-2018-17'
segment = '1524125937193.1'
number = 'CC-MAIN-20180420081400-20180420101400-00000'
MAIN_URL = 'https://data.commoncrawl.org'
url = 'https://data.commoncrawl.org/crawl-data/{DATA_PACKET}/segments/{segment}/warc/{number}.warc.gz'
path_to_load_dump = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_dumps'


def _download_dumps(dump_name: str) -> None:
    command = ['wget', MAIN_URL + '/' + dump_name, '-P', path_to_load_dump]
    subprocess.run(command)


def read_paths_file_and_download_dumps(warc_paths_file: str, read_count: int = None):
    with gzip.open(warc_paths_file, 'rt') as file_reader:
        for number_line, dump_part in enumerate(file_reader):
            _download_dumps(dump_part.strip('\n'))
            if read_count and number_line > read_count:
                break


class LogicError(Exception):
    pass


structure_template = {
    "lang": "language",
    "": "",
}


# def process_response_record(record: ArcWarcRecord) -> None:
#     # print(record.format)
#     print(record.http_headers.__dict__.get('statusline'))
#     status_line = record.http_headers.__dict__.get('statusline')
#     if status_line in ('301 Moved Permanently', '302 Found',
#                        '302 Redirect', '410 Gone', '404 Not Found',
#                        '301 Moved', '500 Internal Server Error',
#                        '303 See Other', '404', '500',
#                        '308 Permanent Redirect',
#                        '308 Permanent Redirect',
#                        '302 Object moved', '301'):
#         continue
#     if status_line in ('200', '200 OK'):
#         try:
#             content = record.raw_stream.read().decode('utf-8')
#             if len(content) == 0:
#                 continue
#             if 'lang="en"' not in content or 'lang="ru"' not in content:
#                 continue
#             with open(
#                     f'/home/skartavykh/MyProjects/media-bot/storage/data_from_warc/{time.time_ns()}_content_from_dump.html',
#                     'w') as f:
#                 f.write(content)
#         except UnicodeDecodeError:
#             print('error with decoding file')
#     # break


def get_path_to_save_content(file_name: str = None) -> str:
    return f'/home/skartavykh/MyProjects/media-bot/storage/data_from_warc/{time.time_ns()}_content_from_dump.html'


def read_dump_packet_file(path: str):
    record_types = set()
    records_counters = defaultdict(int)
    all_statuses = ('301 Moved Permanently', '302 Found', '302 Redirect', '410 Gone', '404 Not Found', '301 Moved',
                    '500 Internal Server Error', '303 See Other', '404', '500', '308 Permanent Redirect',
                    '308 Permanent Redirect',
                    '302 Object moved', '301')
    with open(path, 'rb') as stream:
        for record in ArchiveIterator(stream):
            record_types.add(record.rec_type)

            record: ArcWarcRecord = record
            record_type = record.rec_type
            records_counters[record_type] += 1
            if record_type == 'response':
                # print(record.http_headers.__dict__)
                status_line = record.http_headers.__dict__.get('statusline')
                if status_line in all_statuses:
                    continue
                # print(record.http_headers.__dict__.get('statusline'))
                if status_line in ('200', '200 OK'):
                    try:
                        content = record.raw_stream.read().decode('utf-8')
                        if len(content) == 0:
                            continue
                        if 'lang="en"' not in content or 'lang="ru"' not in content:
                            continue
                        print(content[:32])
                        # with open(get_path_to_save_content(), 'w') as f:
                        #     f.write(content)
                    except UnicodeDecodeError:
                        print('error with decoding file')
                # break
            elif record_type == 'metadata':
                # content = record.raw_stream.read().decode('utf-8')
                # print(record.http_headers)
                # print(content)
                pass
            elif record_type == 'revisit':
                pass
            elif record_type == 'warcinfo':
                content = record.raw_stream.read().decode('utf-8')
                # print(record.http_headers)
                # print(record.rec_headers)
            elif record_type == 'request':
                pass
            else:
                raise LogicError('Unknown type of record in warc file!')
    print('record types:', record_types)
    print('records count:', records_counters)


def get_dump_path(warc_file_name: str) -> str:
    return '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/' + warc_file_name


if __name__ == '__main__':
    # read_dump_packet_file(get_dump_path('CC-MAIN-20240802234508-20240803024508-00000.warc.gz'))
    # read_paths_file_and_download_dumps('/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/news_paths.gz')
    read_paths_file_and_download_dumps('/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc.paths.gz',
                                       read_count=15)
