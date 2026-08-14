from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None
class CategoryCreate(CategoryBase):
    """Schema for create category"""
    pass

class CategoryUpdate(CategoryBase):
    """Schema for update category"""
    name: str | None = None
    description: str | None = None

class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
           from_attributes = True
class Category(CategoryInDBBase):
    """Schema return category"""
    pass