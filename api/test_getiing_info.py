import os
import json

from dotenv import load_dotenv
import requests

load_dotenv()

NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')

url = ('https://newsapi.org/v2/top-headlines?'
       'sources=bbc-news&'
       f'apiKey={NEWS_API_KEY}')
response = requests.get(url)

with open('/home/sklion/projects/media-bot/storage/file.json', 'w') as f:
    json.dump(response.json(), f, indent=4)
