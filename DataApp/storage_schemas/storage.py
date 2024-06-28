import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import create_engine


engine = create_engine("postgresql://admin:password@localhost:5500/storage", echo=True)


class Base(DeclarativeBase):
    pass


COMMON_SCHEMA = "articles"


class Block(Base):
    __tablename__ = "block"
    __table_args__ = {"schema": COMMON_SCHEMA}

    block_id: Mapped[int] = mapped_column(primary_key=True)
    priority: Mapped[int]
    short_title: Mapped[str]


class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {"schema": COMMON_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str | None]
    title: Mapped[str | None]
    description: Mapped[str | None]
    content: Mapped[str | None]
    published_at: Mapped[datetime.datetime]
    url: Mapped[str] = mapped_column(unique=True)


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
