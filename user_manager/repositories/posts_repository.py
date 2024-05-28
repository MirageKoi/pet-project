from dataclasses import dataclass

from asyncpg import Pool
from models.posts import Post, PostCreate

from .repository import IRepository


class ObjectDoesNotExist(Exception):
    pass


@dataclass
class PostsRepository(IRepository):
    pool: Pool

    async def all(self) -> list[Post]:
        async with self.pool.acquire() as connection:
            records = await connection.fetch("SELECT * FROM posts")
            return [Post.model_validate(dict(record)) for record in records]

    async def get(self, post_id: int) -> Post:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow("SELECT * FROM posts WHERE post_id = $1", post_id)
            if not record:
                raise ObjectDoesNotExist(f"Post with id {post_id} does not exist.")
            return Post.model_validate(dict(record))

    async def create(self, item: PostCreate) -> Post:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """INSERT INTO posts (user_id, title, content, created_at) VALUES ($1, $2, $3, $4) RETURNING *""",
                item.user_id,
                item.title,
                item.content,
                item.created_at,
            )
            return Post.model_validate(dict(record))

    async def update(self, post_id: int, item: Post) -> Post:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """UPDATE posts SET user_id = $1, title = $2, content = $3 WHERE post_id = $4 RETURNING *""",
                item.user_id,
                item.title,
                item.content,
                post_id,
            )
            return Post.model_validate(dict(record))

    async def delete(self, post_id: int):
        async with self.pool.acquire() as connection:
            value = await connection.execute("""DELETE FROM posts WHERE post_id = $1""", post_id)
            return int(value.split()[1])
