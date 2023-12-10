import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')

url_everything = 'https://newsapi.org/v2/everything'
everything_payload = {
    'q': 'bitcoin',
    'apiKey': NEWS_API_KEY,
}
response = requests.get(url_everything, params=everything_payload)

with open('/home/skartavykh/PycharmProjects/media-bot/storage/testfile.json', 'w') as f:
    json.dump(response.json(), f, indent=4)
