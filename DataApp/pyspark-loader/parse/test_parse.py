import functools
import os
import time
from collections import defaultdict
from enum import IntEnum
from multiprocessing import Pool
from typing import Iterable, Any

from dotenv import load_dotenv

import html_to_json
from fastwarc.stream_io import GZipStream
from fastwarc.warc import ArchiveIterator, WarcRecordType
from resiliparse.parse.html import HTMLTree
from resiliparse.parse.encoding import detect_encoding

from db_manager import engine
from sqlalchemy.orm import Session

from db_models import ParsedPacket


load_dotenv()

WARC_FILES_DIR = os.getenv('WARC_FILES_DIR')


def get_default_metadata() -> dict:
    return {'count_processed_records': 0,
            'languages_codes': defaultdict(int),
            'count_appropriate_records': 0,
            'NO_URL_IN_WARC-Target-URI': 0,
            'pages_without_doctype': 0}


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
source_link_flag = '<link rel="canonical" href='


def _get_canonical_link(content_html: str) -> str | None:
    start_url_index = content_html.find(source_link_flag) + len(source_link_flag) + 1
    if start_url_index == -1:
        return None
    end_url_index = content_html.find('"', start_url_index)
    return content_html[start_url_index:end_url_index]


def process_html(content_string: str) -> dict[str, Any]:
    canon_link = _get_canonical_link(content_html=content_string)

    structure_json = html_to_json.convert(content_string)
    status_error = None

    try:
        title = structure_json['html'][0]['head'][0]['title'][0]['_value']
    except KeyError:
        status_error = ProcessingHTMLStatusCode.error_no_title
        title = None

    links = []
    main_link = None

    def traverse(struct: Any) -> None:
        nonlocal main_link
        if isinstance(struct, (int, str)):
            return
        if isinstance(struct, dict):
            for key, _ in struct.items():
                if key == "href":
                    condition_on_link = isinstance(struct[key], str) and struct[key].startswith('http')
                    if condition_on_link:
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
    result['pageTitle'] = title if title else "NO TITLE"
    result['canonicalLink'] = canon_link
    return result


def process_warc_file(file_path: str, limit_records: int = -1, write_raw_html: bool = False) -> Iterable:
    warc_file_label = file_path[file_path.find('CC-NEWS-') + len('CC-NEWS-'):].strip('.warc.gz')
    _metadata = getattr(process_warc_file, 'metadata', get_default_metadata())
    pages_without_doctype = 0
    with open(file_path, 'rb') as file:
        stream = GZipStream(file)
        file_iterator = ArchiveIterator(stream, record_types=WarcRecordType.response | WarcRecordType.request,
                                        parse_http=True)
        for entry_number, record in enumerate(file_iterator):
            if limit_records != -1:
                if entry_number > limit_records:
                    break
            _metadata['count_processed_records'] += 1
            record_reader = record.reader
            content: bytes = record_reader.read()
            html_tree = HTMLTree.parse_from_bytes(content, detect_encoding(content))
            content_string = str(html_tree.document)
            if write_raw_html:
                save_to = f'/home/skartavykh/MyProjects/media-bot/storage/raw_html_dump/raw_html_{time.time_ns()}.html'
                with open(save_to, 'w') as f:
                    f.write(content_string)
            if not content_string.startswith('<!DOCTYPE'):
                pages_without_doctype += 1
                continue
            headers_dict = {str(k): v for k, v in record.headers}
            url = headers_dict.get('WARC-Target-URI')
            if url is None:
                _metadata['NO_URL_IN_WARC-Target-URI'] += 1
            meta = html_tree.document.query_selector('html')
            language = None
            if meta is not None:
                language = meta.getattr('lang')
            if language in ('ru', 'en', 'en-US', 'ru-ru', 'en-us', 'EN'):
                _metadata['count_appropriate_records'] += 1
                processed_html_content = process_html(content_string)
                processed_html_content['warc_file_id'] = warc_file_label
                yield processed_html_content
            else:
                _metadata['languages_codes'][language] += 1
    _metadata['pages_without_doctype'] += 1


def process_one_warc_file(warc_file_name: str, records: int = 100, debug: bool = False, delete_file: bool = False) -> int:
    params = {"file_path": WARC_FILES_DIR + warc_file_name,
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
    if delete_file:
        # TODO Create entry in configuration database or write in log file that warc-file is successfully processed.
        print('LOG(PROCESSING SUCCESSFULLY): WARC file:', warc_file_name, 'is processed!')
        if os.path.exists(WARC_FILES_DIR + warc_file_name):
            os.remove(WARC_FILES_DIR + warc_file_name)
    return GeneralStatusCode.success


def run_tasks_with_multiprocessing_pool(workers: int = 1) -> None:
    process_one_warc_file_partial = functools.partial(process_one_warc_file, records=-1)
    warc_dump_files = reversed(os.listdir(WARC_FILES_DIR))
    with Pool(processes=workers) as process_pool:
        process_pool.map(process_one_warc_file_partial, warc_dump_files)


def debug_process_warc_file() -> None:
    process_warc_file.metadata = {'count_processed_records': 0,
                                  'languages_codes': defaultdict(int),
                                  'count_appropriate_records': 0,
                                  'NO_URL_IN_WARC-Target-URI': 0,
                                  'pages_without_doctype': 0}
    try:
        iterator = process_warc_file(file_path=WARC_FILES_DIR + 'CC-NEWS-20240101002957-01499.warc.gz',
                                     limit_records=1000)
        for i, json_struct in enumerate(iterator):
            # link: str = json_struct['link']
            # if not link.startswith('http'):
            #     print(json_struct)
            # print(i, json_struct)
            print(i)
    except KeyboardInterrupt:
        print("MAIN_LINKS_NOT_FOUND", MAIN_LINKS_NOT_FOUND)
    metadata = process_warc_file.metadata
    # print('count_processed_records', metadata['count_processed_records'])
    # print('unknown_languages_codes', dict(metadata['languages_codes']))
    # print('count_appropriate_records', metadata['count_appropriate_records'])
    # print('No URL in WARC-Target-URI', metadata['NO_URL_IN_WARC-Target-URI'])
    # print('pages_without_doctype', metadata['pages_without_doctype'])


if __name__ == '__main__':
    run_tasks_with_multiprocessing_pool(workers=4)
    # debug_process_warc_file()
