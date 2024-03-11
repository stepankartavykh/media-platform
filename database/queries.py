import inspect
import os

from database.services.source.service import SourceService
from database.services.topic.service import TopicService
from database.services.user.service import UserService

script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def add_user_query(user_id, name):
    UserService().add_user(user_id, name)


def add_source_query(user_id, url):
    SourceService().add_source(user_id, url)


def add_topic_query(id_, pid, name, rank):
    TopicService().add_topic(id_, pid, name, rank)


def get_user(user_id):
    return UserService().get_user(user_id)


def get_sources(user_id):
    SourceService.get_sources_for_user(user_id)


def get_topics(user_id):
    TopicService().get_topics_for_user(user_id)
