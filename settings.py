# coding: utf-8
from configparser import ConfigParser
from os import path
from typing import Dict


def get_settings_from_config(config_uri: str) -> Dict[str, str]:
    config = ConfigParser()
    config.optionxform = str
    config.read(config_uri)
    return dict(config.items('app:main'))


PROJECT_DIRECTORY = path.dirname(path.dirname(path.abspath(__file__)))
# BASE_DIRECTORY = path.join(PROJECT_DIRECTORY, 'app')
CONFIG_PATH = path.join(PROJECT_DIRECTORY, 'development.ini')
SETTINGS = get_settings_from_config(CONFIG_PATH)
