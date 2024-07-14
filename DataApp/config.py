import os
import inspect
import configparser
from enum import Enum
import psycopg2
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


class DatabaseConfig(Enum):
    host = POSTGRES_HOST
    port = POSTGRES_PORT
    user = POSTGRES_USER
    password = POSTGRES_PASSWORD
    database_name = POSTGRES_DATABASE_NAME

    @classmethod
    def check(cls) -> None:
        with psycopg2.connect(dbname=cls.database_name.value,
                              host=cls.host.value,
                              user=cls.user.value,
                              password=cls.password.value,
                              port=cls.port.value):
            print('Connection to config database is established!')

    @classmethod
    def get_config_url(cls, driver: str = '') -> str:
        url_pattern = '{dialect}{driver}://{username}:{password}@{host}:{port}/{database}'
        return url_pattern.format(dialect='postgresql',
                                  driver=driver,
                                  username=cls.user.value,
                                  password=cls.password.value,
                                  host=cls.host.value,
                                  port=cls.port.value,
                                  database=cls.database_name.value)


LOCAL_STORAGE_PATH = MAIN_DIR + STORAGE_PATH

load_dotenv()

IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')

BOT_TOKEN = os.getenv('BOT_TOKEN')
NEWS_API_KEY = os.getenv('API_NEWS_FEED_KEY')
NEWS_DATA_IO_KEY = os.getenv('NEWS_DATA_IO_KEY')
CACHE_SYSTEM_HOST = os.getenv('CACHE_SYSTEM_HOST')
CACHE_SYSTEM_PORT = os.getenv('CACHE_SYSTEM_PORT')


class MessageBrokerConfig(Enum):
    host = os.getenv('MESSAGE_BROKER_HOST')
    port = os.getenv('MESSAGE_BROKER_PORT')
