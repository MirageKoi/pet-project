from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str

    @property
    def created_at(self):
        return datetime.now()


class PostUpdate(BaseModel):
    user_id: int | None = None
    title: str | None = None
    content: str | None = None


class Post(BaseModel):
    post_id: int
    user_id: int
    title: str
    content: str
    created_at: datetime


class PostList(BaseModel):
    posts: list[Post]
