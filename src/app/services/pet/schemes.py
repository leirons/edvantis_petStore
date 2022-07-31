from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str = " Dogs"


class Tags(BaseModel):
    id: int
    name: str = "Beauty"


class PetBase(BaseModel):
    id: int
    user_id: int
    name: str = "doggie"
    tags: Tags
    category: Category
    status: str = "available"
