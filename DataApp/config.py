import os
import inspect
import configparser
from enum import Enum

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

MESSAGE_BROKER_HOST = config_parser['MESSAGE_BROKER_HOST']
MESSAGE_BROKER_PORT = config_parser['MESSAGE_BROKER_PORT']


class DatabaseConfig(Enum):
    host = POSTGRES_HOST
    port = POSTGRES_PORT
    user = POSTGRES_USER
    password = POSTGRES_PASSWORD
    database_name = POSTGRES_DATABASE_NAME


class MessageBrokerConfig(Enum):
    host = MESSAGE_BROKER_HOST
    port = MESSAGE_BROKER_PORT


LOCAL_STORAGE_PATH = MAIN_DIR + STORAGE_PATH

load_dotenv()

IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')
NEWS_DATA_IO_KEY = os.getenv('NEWS_DATA_IO_KEY')
CACHE_SYSTEM_HOST = os.getenv('CACHE_SYSTEM_HOST')
CACHE_SYSTEM_PORT = os.getenv('CACHE_SYSTEM_PORT')
