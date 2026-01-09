from pydantic import BaseModel, Field

class AuthorCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    bio: str | None = None

class AuthorUpdateSchema(BaseModel):
    name: str | None = Field(None, min_length=1)
    bio: str | None = None

class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    bio: str | None
