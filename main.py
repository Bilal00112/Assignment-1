from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Book
# from schemas import BookCreate

# Initialize Database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI App
app = FastAPI()

# Mount static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📚 Home Page - List Books
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# ➕ Add Book Page
@app.get("/add")
def add_page(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})

# ➕ Add Book - POST
@app.post("/add")
def add_book(title: str = Form(...), author: str = Form(...), genre: str = Form(...),
             price: float = Form(...), publication_year: int = Form(...), db: Session = Depends(get_db)):
    new_book = Book(title=title, author=author, genre=genre, price=price, publication_year=publication_year)
    db.add(new_book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# ✏️ Edit Book Page
@app.get("/edit/{book_id}")
def edit_page(book_id: int, request: Request, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "book": book})

# ✏️ Edit Book - POST
@app.post("/edit/{book_id}")
def edit_book(book_id: int, title: str = Form(...), author: str = Form(...), genre: str = Form(...),
              price: float = Form(...), publication_year: int = Form(...), db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db_book.title, db_book.author, db_book.genre, db_book.price, db_book.publication_year = title, author, genre, price, publication_year
    db.commit()
    return RedirectResponse(url="/", status_code=303)

# 🗑 Delete Book
@app.get("/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
