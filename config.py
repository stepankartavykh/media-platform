import os
import inspect
import configparser
from dotenv import load_dotenv

MAIN_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

config_parser = configparser.ConfigParser()
config_parser.read(MAIN_DIR + '/development.ini')

DATABASE_PATH = config_parser['DEFAULT']['DATABASE_PATH']
STORAGE_PATH = config_parser['DEFAULT']['STORAGE_PATH']

POSTGRES_HOST = config_parser['DEFAULT']['POSTGRES_HOST']
POSTGRES_PORT = config_parser['DEFAULT']['POSTGRES_PORT']
POSTGRES_USER = config_parser['DEFAULT']['POSTGRES_USER']
POSTGRES_PASSWORD = config_parser['DEFAULT']['POSTGRES_PASSWORD']
POSTGRES_DATABASE_NAME = 'postgres'

REDIS_HOST = config_parser['DEFAULT']['REDIS_HOST']
REDIS_PORT = config_parser['DEFAULT']['REDIS_PORT']

LOCAL_STORAGE_PATH = MAIN_DIR + STORAGE_PATH

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')
NEWS_DATA_IO_KEY = os.getenv('NEWS_DATA_IO_KEY')
