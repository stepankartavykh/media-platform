from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.row import Row
from DataApp import DatabaseConfig

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text


class Base(DeclarativeBase):
    pass


CONTENT_SCHEMA = 'actual_content'


class AsyncDatabaseStoragePlugin:
    def __init__(self):
        self.async_engine = create_async_engine(DatabaseConfig.get_config_url('+asyncpg'))
        self.session = async_sessionmaker(self.async_engine, expire_on_commit=False)
        self._check_content_schema()

    def _check_content_schema(self) -> None:
        pass
        # TODO make check function to make sure that service is available

    async def get_actual_content(self) -> Sequence[Row]:
        query = 'SELECT * FROM actual_content.content'
        async with self.async_engine.begin() as connection:
            res: CursorResult = await connection.execute(text(query))
            content_blocks = res.fetchall()
            print(content_blocks)
            return content_blocks
