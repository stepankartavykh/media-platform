import os

from dotenv import load_dotenv

MAIN_DIR = '/home/skartavykh/MyProjects/media-bot'
STORAGE_PATH = '/storage'
load_dotenv('/home/skartavykh/MyProjects/media-bot/api/.env')

IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')
NEWS_DATA_IO_KEY = os.getenv('NEWS_DATA_IO_KEY')
CACHE_SYSTEM_HOST = os.getenv('CACHE_SYSTEM_HOST')
CACHE_SYSTEM_PORT = os.getenv('CACHE_SYSTEM_PORT')


if __name__ == '__main__':
    print(NEWS_API_KEY)
