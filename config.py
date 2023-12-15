import os
import inspect
import configparser
from dotenv import load_dotenv

MAIN_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

config_parser = configparser.ConfigParser()
config_parser.read(MAIN_DIR + '/development.ini')

DATABASE_PATH = config_parser['DEFAULT']['DATABASE_PATH']
STORAGE_PATH = config_parser['DEFAULT']['STORAGE_PATH']

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')
