import io

import requests
import warcio


def prog():
    warc_filename = 'crawl-data/CC-MAIN-2021-10/segments/1614178365186.46/warc/CC-MAIN-20210303012222-20210303042222-00595.warc.gz'
    warc_record_offset = 250975924
    warc_record_length = 6922

    response = requests.get(f'https://data.commoncrawl.org/{warc_filename}',
                            headers={'Range': f'bytes={warc_record_offset}-{warc_record_offset + warc_record_length - 1}'})

    with io.BytesIO(response.content) as stream:
        for record in warcio.ArchiveIterator(stream):
            html = record.content_stream().read()

    print(html.decode('utf-8'))


def ppp():
    import requests
    import pathlib
    import json
    from pprint import pprint

    news_website_base = 'hobbsnews.com'
    URL = "https://index.commoncrawl.org/CC-MAIN-2022-05-index?url=" + news_website_base + "/*&output=json"
    website_output = requests.get(URL)
    pathlib.Path('data.json').write_bytes(website_output.content)

    news_articles = []
    test_article_num = 300
    for line in open('data.json', 'r'):
        news_articles.append(json.loads(line))

    pprint(news_articles[test_article_num])

    news_URL = news_articles[test_article_num]['url']
    news_warc_file = news_articles[test_article_num]['filename']
    news_offset = news_articles[test_article_num]['offset']
    news_length = news_articles[test_article_num]['length']


def main():
    crawl_dump = 'CC-MAIN-2024-33'
    sources = [
        # 'investopedia.com', 'hobbsnews.com', 'newscientist.com', 'www.sciencedaily.com',
        # 'rbc.ru',
        # 'kommersant.ru',
        'edu'
    ]
    for url_to_find in sources:
        url = f'https://index.commoncrawl.org/{crawl_dump}-index?url={url_to_find}'
        response = requests.get(url)
        print(response.text)


if __name__ == '__main__':
    main()
