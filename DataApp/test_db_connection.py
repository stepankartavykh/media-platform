import asyncio

from database import DBSession
import models

import asyncpg


def get_articles_count(session):
    articles = session.query(models.Article).all()
    return len(articles)


# def insert_some_articles(session):
#     session.

def make_async_query():
    async def main():
        connection = await asyncpg.connect(host='localhost',
                                           port=5500,
                                           user='admin',
                                           database='postgres',
                                           password='password')
        version = connection.get_server_version()
        print(f'PostgreSQL version = {version}')

        res = await connection.execute('''
            SELECT article.title from article;
        ''')
        print(res)

        await connection.close()

    asyncio.run(main())


if __name__ == '__main__':
    print(get_articles_count(DBSession))
    print('=' * 40 + 'End of function get_articles_count' + '=' * 40)
    make_async_query()
