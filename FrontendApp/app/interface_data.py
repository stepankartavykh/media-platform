"""Models for API specification."""
import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UpdateType(Enum):
    replace = 'replace'
    add = 'add'


class SourceInterface(BaseModel):
    id: Optional[int]
    name: str
    update_type: UpdateType


class AddArticleInterface(BaseModel):
    priority: int
    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    published_at: Optional[datetime.datetime] = Field(alias='publishedAt')
    content: str


class UpdateArticleInterface(BaseModel):
    update_type: str
    priority: int
    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    published_at: datetime.datetime = Field(alias='publishedAt')
    content: str


class DataPacketInterface(BaseModel):
    articlesAdd: Optional[list[AddArticleInterface]]
    articlesUpdate: Optional[list[UpdateArticleInterface]]


class BlockPart(BaseModel):
    id: int
    priority: int
    short_title: str


class Block(BaseModel):
    id: int
    priority: int
    short_title: str = Field(alias='shortTitle')
    short_description: str = Field(alias='shortDescription')
    block_content: Optional[list[BlockPart]] = Field(alias='blockContent')


class AllDataStartState(BaseModel):
    """Interface for loading all content data when user opens first page."""
    blocks: Optional[list[Block]]


def load_json_structure(path: str) -> str:
    with open(path) as f:
        all_content = f.read()
    return all_content
