from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    price: float
    publication_year: int


class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True

