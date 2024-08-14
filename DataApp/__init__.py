from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from DataApp.config import DatabaseConfig


engine_ = create_engine(DatabaseConfig.get_config_url('+asyncpg'))
async_engine = create_async_engine(DatabaseConfig.get_config_url('+asyncpg'))

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
Session = sessionmaker(engine_)


class Base(DeclarativeBase):
    pass
