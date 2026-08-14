from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import authors, categories, book

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Book Management API",
    description="Simple API to manage books, authors, categories and book covers",
    version="1.0.0",
)
#Include routes
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(book.router, prefix="/books", tags=["Books"])

#static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")  
def read_root():
    return {"message": "Book Management API is running"}
