from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from BotApp.database import Base


# TODO configuration for Data mart is required!

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "config"}

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    username: Mapped[Optional[str]]


class Topic(Base):
    """
    rank: number describing in which order give "messages" (compilation of articles). For example 1 is the highest
    priority - if there are two articles with rank 1 and 2, then the article with rank 1 added first
    """
    __tablename__ = "topic"
    __table_args__ = {"schema": "config"}

    id: Mapped[int] = mapped_column(primary_key=True)
    pid: Mapped[int] = mapped_column(ForeignKey("topic.id"), nullable=True)
    name: Mapped[str]
    rank: Mapped[int]


class UserTopic(Base):
    __tablename__ = "user_topic"
    __table_args__ = {"schema": "config"}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"))


class UserSource(Base):
    __tablename__ = "user_source"
    __table_args__ = {"schema": "config"}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"))


class Source(Base):
    __tablename__ = "source"
    __table_args__ = {"schema": "config"}

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(unique=True)
    name: Mapped[Optional[str]]


class Subscriber(Base):
    __tablename__ = "subscriber"
    __table_args__ = {"schema": "config"}

    subscriber_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    chat_id: Mapped[int]


class Article(Base):
    __tablename__ = "article"
    __table_args__ = {"schema": "storage"}

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[str | None]
    title: Mapped[str | None]
    description: Mapped[str | None]
    content: Mapped[str]
