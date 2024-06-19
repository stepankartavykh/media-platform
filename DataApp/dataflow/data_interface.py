import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UpdateType(Enum):
    replace = 'replace'
    add = 'add'


class SourceInterface(BaseModel):
    id: Optional[str]
    name: str
    update_type: UpdateType


class AddArticleInterface(BaseModel):
    priority: int
    source: SourceInterface
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str] = Field(alias='urlToImage')
    published_at: datetime.datetime = Field(alias='publishedAt')
    content: str


class UpdateArticleInterface(BaseModel):
    update_type: UpdateType
    priority: int
    source: SourceInterface
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str] = Field(alias='urlToImage')
    published_at: datetime.datetime = Field(alias='publishedAt')
    content: str


class DataPacketInterface(BaseModel):
    articlesAdd: list[AddArticleInterface]
    articlesUpdate: list[UpdateArticleInterface]
