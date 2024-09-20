from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("postgresql://admin:password@localhost:5500/storage", echo=True)


class DatabaseManagerWARC:
    def __init__(self, _engine):
        self.engine = _engine

    def __enter__(self):
        print('enter DatabaseManagerWARC...')
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit DatabaseManagerWARC...')
        pass


if __name__ == '__main__':
    with DatabaseManagerWARC(engine) as warc_db_manager:
        print('some code')
