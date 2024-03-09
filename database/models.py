from typing import Optional
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    fullname: Mapped[Optional[str]]


class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[Optional[str]]
    content: Mapped[Optional[str]]


class Topic(Base):
    __tablename__ = "topic"
    id: Mapped[int] = mapped_column(primary_key=True)
    pid: Mapped[int] = mapped_column(ForeignKey("topic.id"))
    name: Mapped[str]
    rank: Mapped[int]


class UserTopic(Base):
    __tablename__ = "user_topic"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"))
