import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine


engine = create_engine("postgresql://admin:password@localhost:5500/storage", echo=True)
async_engine = create_async_engine("postgresql+asyncpg://admin:password@localhost:5500/storage", echo=True)


class Base(DeclarativeBase):
    pass


ARTICLES_COMMON_SCHEMA = "articles"
RESOURCE_COMMON_SCHEMA = "resources"
PARSED_DATA_COMMON_SCHEMA = "parsed"
FRONTEND_CONTENT_SCHEMA = "actual_content"
EVENTS_SCHEMA = "events"


class ArticleBlock(Base):
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


class ParsedPacket(Base):
    __tablename__ = "packets"
    __table_args__ = {"schema": PARSED_DATA_COMMON_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    packet: Mapped[dict] = mapped_column(JSONB)


class Block(Base):
    __tablename__ = "block"
    __table_args__ = {"schema": FRONTEND_CONTENT_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[int]
    short_title: Mapped[str]
    short_description: Mapped[str]

    items: Mapped[list["BlockContent"]] = relationship(back_populates="parent_block")


class BlockContent(Base):
    __tablename__ = "block_item"
    __table_args__ = {"schema": FRONTEND_CONTENT_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[int]
    block_id: Mapped[int] = mapped_column(ForeignKey(Block.id))
    title: Mapped[str | None]
    description: Mapped[str | None]
    content: Mapped[str | None]
    links: Mapped[str]

    parent_block: Mapped["Block"] = relationship(back_populates="items")


class Event(Base):
    __tablename__ = "event"
    __table_args__ = {"schema": EVENTS_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_datetime: Mapped[datetime.datetime] = mapped_column(insert_default=func.utc_timestamp(), nullable=False,
                                                              server_default=func.now())


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
