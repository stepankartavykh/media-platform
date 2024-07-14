from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from DataApp.config import DatabaseConfig


engine_ = create_engine(DatabaseConfig.get_config_url('+asyncpg'))
Session = sessionmaker(engine_)


class Base(DeclarativeBase):
    pass
