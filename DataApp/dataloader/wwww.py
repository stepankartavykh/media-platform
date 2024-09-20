import requests
import json

from urllib.parse import quote_plus

from warcio.archiveiterator import ArchiveIterator

SERVER = 'http://index.commoncrawl.org/'
INDEX_NAME = 'CC-MAIN-2024-33'
target_url = 'www.washingtonpost.com'


def search_cc_index(url):
    encoded_url = quote_plus(url)
    index_url = f'{SERVER}{INDEX_NAME}-index?url={encoded_url}&output=json'
    response = requests.get(index_url)
    print("Response from server:\r\n", response.text)
    if response.status_code == 200:
        records = response.text.strip().split('\n')
        return [json.loads(record) for record in records]
    else:
        return None


def fetch_page_from_cc(records):
    for record in records:
        offset, length = int(record['offset']), int(record['length'])
        s3_url = f'https://data.commoncrawl.org/{record["filename"]}'

        byte_range = f'bytes={offset}-{offset+length-1}'

        response = requests.get(
            s3_url,
            headers={'Range': byte_range},
            stream=True
        )

        if response.status_code == 206:
            stream = ArchiveIterator(response.raw)
            for warc_record in stream:
                if warc_record.rec_type == 'response':
                    return warc_record.content_stream().read()
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None

    print("No valid WARC record found in the given records")
    return None


if __name__ == '__main__':
    records = search_cc_index(target_url)
    if records:
        print(f"Found {len(records)} records for {target_url}")
        content = fetch_page_from_cc(records)
        if content:
            print(f"Successfully fetched content for {target_url}")
    else:
        print(f"No records found for {target_url}")
