from pydantic import BaseModel, field_validator
from typing import List


class BookCreateSchema(BaseModel):
    title: str
    year: int
    pages: int
    publisher: str | None = None
    author_ids: List[int] = []

    @field_validator("title", "publisher")
    def strip_whitespace(cls, v):
        if v is None:
            return v
        return v.strip()


class BookUpdateSchema(BaseModel):
    title: str | None = None
    year: int | None = None
    pages: int | None = None
    publisher: str | None = None
    author_ids: List[int] | None = None

    @field_validator("title", "publisher")
    def strip_whitespace(cls, v):
        if v is None:
            return v
        return v.strip()


class BookResponseSchema(BaseModel):
    id: int
    title: str
    year: int
    pages: int
    publisher: str | None
    authors: list  # list of dicts from Author.to_dict()
