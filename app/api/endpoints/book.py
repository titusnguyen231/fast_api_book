from fastapi import APIRouter 

router = APIRouter()

@router.get("/")
def list_books():
    return {"message": "List of books do it later"}