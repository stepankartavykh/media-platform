import time
import json


def write_some_files(storage_path_dir: str,
                     headers: dict = None,
                     http_headers: dict = None,
                     warc_json_pages: dict = None):
    if headers is not None:
        with open(f'{storage_path_dir}/warcdata/headers_{time.time()}.json', 'w') as f:
            json.dump(headers, f, indent=4, ensure_ascii=False)
    if http_headers is not None:
        with open(f'{storage_path_dir}/warcdata/http_headers_{time.time()}.json', 'w') as f:
            json.dump(http_headers, f, indent=4, ensure_ascii=False)
    if warc_json_pages is not None:
        with open(f'{storage_path_dir}/json_from_html/warc_records_json_{time.time()}.json',
                  'w') as f:
            json.dump(warc_json_pages, f, indent=4, ensure_ascii=False)
