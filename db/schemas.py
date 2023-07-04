from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    token: str
    username: str
    email: EmailStr 
    password: str
    posts: List[int] = []

class Post(BaseModel):
    author: str
    content: str
    id: int
    likes: List[str] = []
    dislikes: List[str] = []
    
class Like(BaseModel):
    user: str
    post: int

class DisLike(BaseModel):
    username: str
    post: int
