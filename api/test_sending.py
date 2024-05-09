import json
import requests

from api.get_news_dump import get_news_feed_everything

request_to_send_message_directly_url = \
    'https://api.telegram.org/bot{api_bot_token}/sendMessage?chat_id={chat_id_int}&text={message_text_to_send}'


def send(queries: list[str]):
    paths = [
        get_news_feed_everything(query)
        for query in queries
    ]

    for path in paths:
        with open(path) as f:
            data = json.load(f)
        if data['status'] != 'ok':
            print('api key is missing')
            continue
        articles: list = data['articles'][:20]
        # for article in articles:
        # text_message = '\n'.join([(article.get('title', 'No title') + '\n' + article.get('url', 'No url')) for article in articles])
        text_message = '\n'.join([f'<a href="{article.get("url")}">{article.get("title", "No title")}</a>' for article in articles])
        url = request_to_send_message_directly_url.format(api_bot_token='5778832122:AAF3g0PlKrhM7snqNZgl50JeC1X4lXzxc2Y',
                                                          chat_id_int=466965723,
                                                          message_text_to_send=text_message)
        response = requests.get(url)
        print(response.status_code)


def send_message_to_chat(message: str, chat_id: int, ):
    url = request_to_send_message_directly_url.format(api_bot_token=API_BOT_TOKEN,
                                                      chat_id_int=chat_id,
                                                      message_text_to_send=message)
    response = requests.get(url)


if __name__ == '__main__':
    send(['hoax', 'conspiracy', 'ai fake'])
