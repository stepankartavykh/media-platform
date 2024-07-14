import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_engine("postgresql://admin:password@localhost:5500/storage", echo=True)
async_engine = create_async_engine("postgresql+asyncpg://admin:password@localhost:5500/storage", echo=True)


class Base(DeclarativeBase):
    pass


ARTICLES_COMMON_SCHEMA = "articles"
RESOURCE_COMMON_SCHEMA = "resources"


class Block(Base):
    __tablename__ = "block"
    __table_args__ = {"schema": ARTICLES_COMMON_SCHEMA}

    block_id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[int]
    short_title: Mapped[str]


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {"schema": ARTICLES_COMMON_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str | None]
    title: Mapped[str | None]
    description: Mapped[str | None]
    content: Mapped[str | None]
    published_at: Mapped[datetime.datetime]
    url: Mapped[str] = mapped_column(unique=True)


class Resource(Base):
    __tablename__ = "common"
    __table_args__ = {"schema": RESOURCE_COMMON_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    base_url: Mapped[str] = mapped_column(unique=True)
    subject: Mapped[str | None]
    category: Mapped[str | None]


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
