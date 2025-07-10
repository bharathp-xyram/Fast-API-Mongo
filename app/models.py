from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    age: int

class UpdateUser(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]