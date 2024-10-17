import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

PARSED_DATA_COMMON_SCHEMA = "parsed"


class Base(DeclarativeBase):
    pass


class ParsedPacket(Base):
    __tablename__ = "packets"
    __table_args__ = {"schema": PARSED_DATA_COMMON_SCHEMA}

    id: Mapped[int] = mapped_column(primary_key=True)
    packet: Mapped[dict] = mapped_column(JSONB)
    appearance_date: Mapped[datetime.datetime] = mapped_column(insert_default=func.now(), nullable=False,
                                                               server_default=func.now())
