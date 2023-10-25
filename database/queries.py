import sqlite3


insert_user_query = "INSERT INTO users (id, fullname) VALUES (?, ?)"
insert_source_query = "INSERT INTO sources (user_id, url) VALUES (?, ?)"
get_sources_query = "SELECT sources.url FROM sources WHERE sources.user_id = (?)"


def add_user_query(user_id, name):
    with sqlite3.connect('/home/skartavykh/PycharmProjects/media-bot/database/db.sqlite') as connection:
        cur = connection.cursor()
        cur.execute(insert_user_query, (user_id, name))
        connection.commit()


def add_source_query(user_id, url):
    with sqlite3.connect('/home/skartavykh/PycharmProjects/media-bot/database/db.sqlite') as connection:
        cur = connection.cursor()
        cur.execute(insert_source_query, (user_id, url))
        connection.commit()


def get_sources(user_id):
    sources = None
    with sqlite3.connect('/home/skartavykh/PycharmProjects/media-bot/database/db.sqlite') as connection:
        cur = connection.cursor()
        cur.execute(get_sources_query, (user_id, ))
        sources = [source[0] for source in cur.fetchall()]
        connection.commit()
    return sources
