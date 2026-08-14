from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None
class AuthorCreate(AuthorBase):
    """Schema for create Author"""
    pass

class AuthorUpdate(AuthorBase):
    """Schema for update Author"""
    name: str | None = None
    bio: str | None = None

class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        from_attributes = True

class Author(AuthorInDBBase):
    """Schema return Author"""
    pass