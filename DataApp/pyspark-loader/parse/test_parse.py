import functools
import os
from collections import defaultdict
from enum import IntEnum
from multiprocessing import Pool
from typing import Iterable, Callable, Any

import html_to_json
from fastwarc.stream_io import GZipStream
from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse.html import HTMLTree
from resiliparse.parse.encoding import detect_encoding

from .db_manager import engine
from sqlalchemy.orm import Session

from .db_models import ParsedPacket


WARC_FILES_DIR = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_dumps/'


class BytesContentError(Exception):
    pass


def process_bytes_data(data: bytes) -> str:
    for encoding in ('utf-8', 'utf-16', 'utf-16-le'):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError as exc:
            print(exc)
            continue
    raise BytesContentError('Data can\'t be decoded')


class GeneralStatusCode(IntEnum):
    success = 100
    error = 500


class ProcessingHTMLStatusCode(IntEnum):
    success = 100
    success_with_no_main_link = 101
    error = 500
    error_no_title = 501


MAIN_LINKS_NOT_FOUND = 0


def process_html(content_string: str) -> dict[str, Any]:
    structure_json = html_to_json.convert(content_string)
    status_error = None

    try:
        title = structure_json['html'][0]['head'][0]['title'][0]['_value']
    except KeyError:
        status_error = ProcessingHTMLStatusCode.error_no_title
        title = None

    links = []
    main_link = None

    def traverse(struct):
        nonlocal main_link
        if isinstance(struct, (int, str)):
            return
        if isinstance(struct, dict):
            for key, _ in struct.items():
                if key == "href":
                    if isinstance(struct[key], str) and struct[key].startswith('http'):
                        links.append(struct[key])
                if struct.get('_attributes') and struct['_attributes'].get('rel') and struct['_attributes'].get('href') \
                        and struct['_attributes']['rel'][0] == 'canonical':
                    main_link = struct['_attributes']['href']
                traverse(struct[key])
        if isinstance(struct, list):
            for item in struct:
                traverse(item)

    traverse(structure_json)

    global MAIN_LINKS_NOT_FOUND

    if main_link is None:
        MAIN_LINKS_NOT_FOUND += 1

    result = {}
    if status_error is None:
        if main_link is None:
            status = ProcessingHTMLStatusCode.success_with_no_main_link
        else:
            status = ProcessingHTMLStatusCode.success
    else:
        status = status_error
    result['status'] = status
    if main_link is not None:
        result['link'] = main_link
    result['title'] = title if title else "NO TITLE"
    return result


source_link_flag = '<link rel="canonical" href='


def get_canonical_link(content_html: str) -> str | None:
    start_url_index = content_html.find(source_link_flag) + len(source_link_flag) + 1
    if start_url_index == -1:
        return None
    end_url_index = content_html.find('"', start_url_index)
    return content_html[start_url_index:end_url_index]


def process_warc_file(file_path: str, limit_records: int = -1, return_iterator: bool = False) -> Iterable:
    languages_codes = defaultdict(int)
    count_appropriate_records = 0
    with open(file_path, 'rb') as file:
        stream = GZipStream(file)
        file_iterator = ArchiveIterator(stream, record_types=WarcRecordType.response | WarcRecordType.request,
                                        parse_http=True)
        for entry_number, record in enumerate(file_iterator):
            if limit_records != -1:
                if entry_number > limit_records:
                    break
            record_reader = record.reader
            content: bytes = record_reader.read()
            html_tree = HTMLTree.parse_from_bytes(content, detect_encoding(content))
            content_string = str(html_tree.document)
            if not content_string.startswith('<!DOCTYPE'):
                continue
            try:
                headers_dict = {str(k): v for k, v in record.headers}
                url = headers_dict['WARC-Target-URI']
                print(url)
            except KeyError:
                print(record.record_type, 'NO URL')
            meta = html_tree.document.query_selector('html')
            language = None
            if meta is not None:
                language = meta.getattr('lang')
            if language in ('ru', 'en', 'en-US', 'ru-ru', 'en-us', 'EN'):
                link = get_canonical_link(content_string)
                print("CANONICAL LINK:", link)
                count_appropriate_records += 1
                processed_html_content = process_html(content_string)
                print(processed_html_content)
                if return_iterator:
                    yield processed_html_content
                else:
                    print(processed_html_content)
            else:
                languages_codes[language] += 1


def process_one_warc_file(warc_file_name: str, records: int = 100, debug: bool = False) -> int:
    params = {"file_path": WARC_FILES_DIR + warc_file_name,
              "return_iterator": True,
              "limit_records": -1}
    if debug:
        for i, item in enumerate(process_warc_file(**params)):
            if i > records:
                break
            print(item)
        return GeneralStatusCode.success
    items_to_add = []
    bucket_records = 10
    with Session(engine) as session:
        try:
            i = 0
            for item in process_warc_file(**params):
                i += 1
                items_to_add.append(ParsedPacket(packet=item))
                if i > bucket_records:
                    session.add_all(items_to_add)
                    session.commit()
                    i = 0
                    items_to_add.clear()
        except KeyboardInterrupt:
            session.commit()
        session.commit()
    return GeneralStatusCode.success


def run_tasks_with_multiprocessing_pool() -> None:
    process_one_warc_file_partial = functools.partial(process_one_warc_file, records=-1, debug=False)
    warc_dump_files = os.listdir(WARC_FILES_DIR)
    with Pool(processes=2) as process_pool:
        process_pool.map(process_one_warc_file_partial, warc_dump_files)


def debug_process_warc_file() -> None:
    try:
        iterator = process_warc_file(file_path=WARC_FILES_DIR + 'CC-NEWS-20240101002957-01499.warc.gz',
                                     limit_records=-1, return_iterator=True)
        for i, _ in enumerate(iterator):
            print(i, "=" * 40)
    except KeyboardInterrupt:
        print("MAIN_LINKS_NOT_FOUND", MAIN_LINKS_NOT_FOUND)


if __name__ == '__main__':
    run_tasks_with_multiprocessing_pool()
