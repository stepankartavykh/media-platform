import inspect
import os
import sqlite3


script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
DATABASE_PATH = script_directory + '/db.sqlite'
insert_user_query = "INSERT INTO users (id, fullname) VALUES (?, ?)"
insert_source_query = "INSERT INTO main.sources (user_id, url) VALUES (?, ?)"
get_sources_query = "SELECT main.sources.url FROM sources WHERE sources.user_id = (?)"
get_user_query = "SELECT id, fullname FROM users WHERE id = (?)"


def add_user_query(user_id, name):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cur = connection.cursor()
        cur.execute(insert_user_query, (user_id, name))
        connection.commit()


def add_source_query(user_id, url):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cur = connection.cursor()
        cur.execute(insert_source_query, (user_id, url))
        connection.commit()


def get_user(user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cur = connection.cursor()
        cur.execute(get_user_query, (user_id, ))
        user = cur.fetchone()
        connection.commit()
    return user


def get_sources(user_id):
    with sqlite3.connect(DATABASE_PATH) as connection:
        cur = connection.cursor()
        cur.execute(get_sources_query, (user_id, ))
        sources = [source[0] for source in cur.fetchall()]
        connection.commit()
    return sources
