import asyncio
from enum import Enum
from typing import Sequence

import psycopg2

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text


class DatabaseConfig(Enum):
    host = 'localhost'
    port = 5500
    user = 'admin'
    password = 'password'
    database_name = 'storage'

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


class Base(DeclarativeBase):
    pass


CONTENT_SCHEMA = 'actual_content'


class AsyncDatabaseStoragePlugin:
    def __init__(self):
        self.async_engine = create_async_engine(DatabaseConfig.get_config_url('+asyncpg'), echo=True)
        self.session = async_sessionmaker(self.async_engine, expire_on_commit=False)
        self._check_content_schema()

    def _check_content_schema(self) -> None:
        pass
        # TODO make check function to make sure that service is available

    async def get_actual_content(self) -> Sequence[Row]:
        query = 'SELECT * FROM actual_content.block'
        async with self.async_engine.begin() as connection:
            res: CursorResult = await connection.execute(text(query))
            content_blocks = res.fetchall()
            return content_blocks

    async def get_packets(self, count: int):
        query = f'SELECT packet FROM parsed.packets ORDER BY appearance_date LIMIT {count}'
        async with self.async_engine.begin() as connection:
            packets_result: CursorResult = await connection.execute(text(query))
            packets = packets_result.fetchall()
            return packets


if __name__ == '__main__':
    plugin = AsyncDatabaseStoragePlugin()
    elements = asyncio.run(plugin.get_packets(100))
    for element in elements:
        print(element[0])
