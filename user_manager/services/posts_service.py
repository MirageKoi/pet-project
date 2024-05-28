from dataclasses import dataclass

from models.posts import Post, PostCreate, PostUpdate
from repositories.posts_repository import PostsRepository


@dataclass
class PostsService:
    posts_repository: PostsRepository

    async def get_post_all(self):
        return await self.posts_repository.all()

    async def get_post_detail(self, post_id: int) -> Post:
        return await self.posts_repository.get(post_id=post_id)

    async def create_post(self, item: dict[str, str]) -> Post:
        post = PostCreate.model_validate(item)
        return await self.posts_repository.create(item=post)

    async def update_post(self, post_id: int, item: dict[str, str]) -> Post:
        db_post = await self.posts_repository.get(post_id=post_id)
        validated_data = PostUpdate.model_validate(item)
        updated_post = db_post.model_copy(update=validated_data.model_dump(exclude_unset=True))
        return await self.posts_repository.update(post_id, updated_post)

    async def delete_post(self, post_id: int):
        await self.posts_repository.get(post_id=post_id)
        result = await self.posts_repository.delete(post_id=post_id)
        return result
