from fastapi import APIRouter, Depends, HTTPException,status, Query
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api.deps import get_db
from app import models
from app.schemas.book import Book, BookCreate, BookUpdate

router = APIRouter()       

@router.get("/",response_model=List[Book])
def list_books(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    author_id: int | None = Query(None),
    category_id: int | None = Query(None),
    year: int | None = Query(None),
    keyword: str | None = Query(None),

):
    """
    Get List book, include filter

    -author_id
    -category_id
    -year (published_year)
    -keyword (search in title or desc)
    """
    mb = models.Book
    query = db.query(models.Book)
    if author_id is not None:
        query = query.filter(mb.author_id == author_id)
    if category_id is not None:
        query = query.filter(mb.category_id == category_id)
    if year is not None:
        query = query.filter(mb.publisher_year == year)
    if keyword is not None:
        like_pattern = f"%{keyword}%"
        query = query.filter(
            or_(
                mb.title.ilike(like_pattern),
                mb.description.ilike(like_pattern),
            )
        )
    
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=Book)
def get_detail_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="book not found"
        )
    return book

@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    db: Session = Depends(get_db)
):
    """Create a new book and check for duplicate names."""
    author = db.query(models.Author).filter(models.Author.id == book_in.author_id).first()

    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author does not exist",
        )

    category = db.query(models.Category).filter(models.Category.id == book_in.category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    book = models.Book(
        title=book_in.title,
        description=book_in.description,
        publisher_year=book_in.publisher_year,
        author_id=book_in.author_id,
        category_id=book_in.category_id,
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book_up: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update book details."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    # Check if author_id is being updated
    if book_up.author_id is not None and book_up.author_id != book.author_id:
        author = db.query(models.Author).filter(models.Author.id == book_up.author_id).first()
        if not author:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Author does not exist",
            )
        book.author_id = book_up.author_id

    # Check if category_id is being updated
    if book_up.category_id is not None and book_up.category_id != book.category_id:
        category = db.query(models.Category).filter(models.Category.id == book_up.category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category does not exist",
            )
        book.category_id = book_up.category_id

    # Update other fields
    if book_up.title is not None:
        book.title = book_up.title

    if book_up.description is not None:
        book.description = book_up.description

    if book_up.publisher_year is not None:
        book.publisher_year = book_up.publisher_year

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """Delete a book."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    db.delete(book)
    db.commit()
