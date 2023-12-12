from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[Optional[str]]


class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))


engine = create_engine("sqlite://", echo=True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
