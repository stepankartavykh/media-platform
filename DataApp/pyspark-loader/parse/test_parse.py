import datetime
import functools
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from enum import IntEnum
from multiprocessing import Pool
from typing import Optional, Iterable, Callable, Any

import fastwarc
import html_to_json
from fastwarc.stream_io import GZipStream
from fastwarc.warc import ArchiveIterator, WarcRecordType, WarcHeaderMap
# import requests
from resiliparse.parse.html import HTMLTree
from resiliparse.parse.encoding import detect_encoding

from db_manager import engine
from sqlalchemy.orm import Session

from db_models import ParsedPacket


class WarcRecordAlias:
    record_id: str
    record_type: WarcRecordType
    content_length: int
    record_date: Optional[datetime]
    headers: WarcHeaderMap
    is_http: bool
    is_http_parsed: bool
    http_headers: Optional[WarcHeaderMap]
    http_content_type: Optional[str]
    http_charset: Optional[str]
    http_date: Optional[datetime.datetime]
    http_last_modified: Optional[datetime.datetime]
    reader: fastwarc.stream_io.BufferedReader
    stream_pos: int


WARC_FILES_DIR = '/home/skartavykh/MyProjects/media-bot/storage/crawled_dumps/warc_dumps/'


# def make_request(url: str) -> str:
#     return requests.get(url, headers=requests.utils.default_headers()).text


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


def process_html_tree(tree: HTMLTree) -> dict[str, Any]:
    # print(tree.document.html)
    # struct = {}
    # urls = []
    # # print(tree.body.text)
    # # print(dir(tree))
    # # print(tree.title)
    #
    # tags = set()
    #
    # def traverse(node: DOMNode):
    #     for child_node in node.child_nodes:
    #         if child_node.tag == 'script':
    #             continue
    #         # print(child_node.text)
    #         if child_node.tag in ('link', 'a'):
    #             pass
    #             # print(child_node.html)
    #         tags.add(child_node.tag)
    #         traverse(child_node)
    #
    # # traverse(tree.body)
    #
    # elements = tree.body.get_elements_by_tag_name('a')
    # # for col in elements:
    # #     print(repr(col.type))
    # #     print(col.child_nodes)
    #
    # coll = tree.body.query_selector_all('main *')
    #
    # # print(repr(coll[0]))
    # #
    # # print(repr(coll[-1]))
    # #
    # # print(repr(coll[:2]))
    #
    # # struct['title'] = tree.title
    # # struct['urls'] = urls
    # return struct
    return {}


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
    # try:
    #     print(structure_json['html'][0]['head'][0]['meta'][0])
    # except (KeyError, TypeError):
    #     pass
    #     # try:
    #     #     print(structure_json['html']['head'])
    #     # except (KeyError, TypeError):
    #     #     print(structure_json['html'])
    # except IndexError:
    #     print("INDEX ERROR:", structure_json['html'][0]['head'][0]['meta'])

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


def write_some_files(headers: dict = None, http_headers: dict = None, warc_json_pages: dict = None):
    if headers is not None:
        with open(f'/home/skartavykh/MyProjects/media-bot/storage/warcdata/headers_{time.time()}.json', 'w') as f:
            json.dump(headers, f, indent=4, ensure_ascii=False)
    if http_headers is not None:
        with open(f'/home/skartavykh/MyProjects/media-bot/storage/warcdata/http_headers_{time.time()}.json', 'w') as f:
            json.dump(http_headers, f, indent=4, ensure_ascii=False)
    if warc_json_pages is not None:
        with open(f'/home/skartavykh/MyProjects/media-bot/storage/json_from_html/warc_records_json_{time.time()}.json',
                  'w') as f:
            json.dump(warc_json_pages, f, indent=4, ensure_ascii=False)


def process_warc_file(file_path: str, limit_records: int = -1, return_iterator: bool = False,
                      debug: bool = False) -> Iterable:
    languages_codes = set()
    count_appropriate_records = 0
    with open(file_path, 'rb') as file:
        stream = GZipStream(file)
        file_iterator = ArchiveIterator(stream, record_types=WarcRecordType.response, parse_http=True)
        for entry_number, record in enumerate(file_iterator):
            if limit_records != -1:
                if entry_number > limit_records:
                    break
            record_reader = record.reader
            content: bytes = record_reader.read()
            # print(process_bytes_data(content))
            html_tree = HTMLTree.parse_from_bytes(content, detect_encoding(content))
            content_string = str(html_tree.document)
            if not content_string.startswith('<!DOCTYPE'):
                continue
                # print('There is no DOCTYPE in content_string!')
                # print(record.record_type)
                # print(content_string)
            # print(record.record_type)
            try:
                headers_dict = {str(k): v for k, v in record.headers}
                url = headers_dict['WARC-Target-URI']
            except KeyError:
                url = None
                print(record.record_type, 'NO URL')
            meta = html_tree.document.query_selector('html')
            language = None
            if meta is not None:
                language = meta.getattr('lang')
            if language in ('ru', 'en', 'en-US', 'ru-ru', 'en-us', 'EN'):
                link = get_canonical_link(content_string)
                # if link in ('ru', 'en'):
                # print(content_string)
                # break
                # print("CANONICAL LINK:", link)
                count_appropriate_records += 1
                # print("LANG:", language)
                # serialized_html_page = process_html_tree(html_tree)
                # serialized_html_page = html_to_json.convert(content_string)
                processed_html_content = process_html(content_string)
                print(processed_html_content)
                if return_iterator:
                    yield processed_html_content
                else:
                    print(processed_html_content)
                # print(processed_html_content)
                # print(serialized_html_page)
                # warc_json_pages[str(record.record_id)] = serialized_html_page
                # record_headers: dict = dict(record.headers)
                # headers[str(record.record_id)] = record_headers
                # record_http_headers: dict = dict(record.http_headers) if record.http_headers else {}
                # http_headers[str(record.record_id)] = record_http_headers
            else:
                languages_codes.add(language)



def process_one_warc_file(warc_file_name: str, records: int = 1000, debug: bool = False) -> int:
    if debug:
        for i, item in enumerate(process_warc_file(file_path=WARC_FILES_DIR + warc_file_name,
                                                   return_iterator=True, limit_records=-1, debug=True)):
            if i > records:
                break
            print(item)
        return GeneralStatusCode.success
    items_to_add = []
    bucket_records = 10
    with Session(engine) as session:
        try:
            i = 0
            for item in process_warc_file(file_path=WARC_FILES_DIR + warc_file_name,
                                          return_iterator=True,
                                          limit_records=-1):
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


def run_tasks_in_process_pool_executor(executor_for_file: Callable, dump_files: list[str]) -> None:
    with ProcessPoolExecutor() as _process_pool:
        _process_pool.map(executor_for_file, dump_files)


def run_tasks_with_multiprocessing_pool() -> None:
    process_one_warc_file_partial = functools.partial(process_one_warc_file, records=-1, debug=False)
    warc_dump_files = os.listdir(WARC_FILES_DIR)
    with Pool(processes=4) as process_pool:
        process_pool.map(process_one_warc_file_partial, reversed(warc_dump_files))


def debug_process_warc_file() -> None:
    try:
        iterator = process_warc_file(file_path=WARC_FILES_DIR + 'CC-NEWS-20240101002957-01499.warc.gz', limit_records=-1,
                                     return_iterator=True, debug=False)
        for i, _ in enumerate(iterator):
            print(i, "=" * 40)
    except KeyboardInterrupt:
        print("MAIN_LINKS_NOT_FOUND", MAIN_LINKS_NOT_FOUND)


if __name__ == '__main__':
    # debug_process_warc_file()
    run_tasks_with_multiprocessing_pool()
