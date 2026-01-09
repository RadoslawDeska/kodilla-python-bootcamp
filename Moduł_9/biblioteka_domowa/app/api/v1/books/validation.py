from pydantic import BaseModel, Field, field_validator

class BookCreateSchema(BaseModel):
    author: str = Field(..., min_length=2, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    year: int = Field(..., ge=0, le=2100)
    pages: int = Field(..., gt=0)
    publisher: str | None = None

    @field_validator("author", "title")
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class BookUpdateSchema(BaseModel):
    author: str | None = Field(None, min_length=2, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)
    year: int | None = Field(None, ge=0, le=2100)
    pages: int | None = Field(None, gt=0)
    publisher: str | None = None

    @field_validator("author", "title")
    def strip_whitespace(cls, v: str) -> str:
        return v.strip() if v else v


class BookResponseSchema(BaseModel):
    id: int
    author: str
    title: str
    year: int
    pages: int
    publisher: str | None
