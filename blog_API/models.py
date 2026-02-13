from sqlmodel import SQLModel, Field

class Blog(SQLModel, table = True):
    id: int | None = Field(None, primary_key = True)
    title: str
    content: str
    category: str