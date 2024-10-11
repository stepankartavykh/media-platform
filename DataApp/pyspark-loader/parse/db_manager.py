from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from sqlalchemy import text


engine = create_engine("postgresql://admin:password@localhost:5500/storage")


class DatabaseManagerWARC:

    __engine = engine

    def __init__(self, _engine: Engine):
        self.engine = _engine

    def __enter__(self):
        print('enter DatabaseManagerWARC...')
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit DatabaseManagerWARC...')
        pass

    @classmethod
    def execute(cls, query: str) -> None:
        with cls.__engine.connect() as connection:
            result = connection.execute(text(query))
            print(result.fetchall())


if __name__ == '__main__':
    with DatabaseManagerWARC(engine) as warc_db_manager:
        print('some code')
    DatabaseManagerWARC.execute('select current_database();')
    DatabaseManagerWARC.execute('select count(*) from parsed.packets;')
