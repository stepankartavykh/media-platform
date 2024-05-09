import inspect
import os

from database.services.source.service import SourceService
from database.services.topic.service import TopicService
from database.services.user.service import UserService

script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def add_user_query(user_id, name):
    UserService().add_user(user_id, name)


def add_source_query(info: dict):
    url = info['source_url']
    source_id = SourceService().get_source_by_url(url)
    if not source_id:
        SourceService().add_source(url=url)
    UserService().add_source_for_user(info.get('user_id'), source_id)


def add_topic_query(pid=1, name='xxx', rank=1):
    TopicService().add_topic(pid, name, rank)


def get_user(user_id):
    return UserService().get_user(user_id)


def get_sources(user_id):
    return [
        'https://www.washingtonpost.com',
        'https://kommersant.ru',
        'https://rbc.ru',
    ]
    # SourceService().get_sources_for_user(user_id)


def get_topics(user_id):
    TopicService().get_topics_for_user(user_id)
