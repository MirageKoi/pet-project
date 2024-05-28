from dataclasses import dataclass
from typing import Any

from models.user import User, UserCreate, UserUpdate
from repositories.users_repository import UsersRepository


@dataclass
class UsersService:
    users_repository: UsersRepository

    async def all(self) -> list[User]:
        result = await self.users_repository.get_all_users()
        return result

    async def get(self, user_id: int) -> User:
        result = await self.users_repository.get_user(user_id=user_id)
        return result

    async def create(self, item: User) -> User:
        validated_data = UserCreate.model_validate(item)
        result = await self.users_repository.create_user(validated_data)
        return result

    async def update(self, user_id: int, item: dict[str, Any]) -> User:
        # 1. Get user by id
        db_user = await self.users_repository.get_user(user_id=user_id)
        # Perform update on some fields
        validated_data = UserUpdate.model_validate(item)
        updated_user = db_user.model_copy(update=validated_data.model_dump(exclude_unset=True))
        # 3. Update in repository
        return await self.users_repository.update_user(item=updated_user)

    async def delete(self, user_id: int) -> int:
        await self.users_repository.get_user(user_id=user_id)
        result = await self.users_repository.delete_user(user_id=user_id)
        return result
