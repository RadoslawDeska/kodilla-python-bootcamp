from pydantic import BaseModel

class BorrowCreateSchema(BaseModel):
    borrower_name: str | None = None
    due_date: str | None = None  # ISO8601
