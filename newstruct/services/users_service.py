from models.user import User, UserCreateValidation
from pydantic.dataclasses import dataclass
from repositories.users_repository import UsersRepository


@dataclass
class UsersService(object):
    users_repository: UsersRepository

    # Get all users
    async def all(self) -> dict:
        result = await self.users_repository.get_all_users()

        return result

    # Get single user
    async def get(self, user_id: int):
        result = await self.users_repository.get_user(user_id=user_id)

        return result

    # Create user
    async def create(self, new_user: UserCreateValidation) -> User:
        result = await self.users_repository.create_user(email=new_user.email, age=new_user.age)
        return result

    # Update user
    async def update(self, user_id: int, kwargs):
        # 1. Get user by id
        user = await self.users_repository.get_user(user_id)

        # Perform update on some fields
        user.email = kwargs.get("email", user.email)
        user.age = int(kwargs.get("age", user.age))

        # 3. Update in repository

        return await self.users_repository.update_user(user)

    # Delete user
    async def delete(self, user_id: int):
        await self.users_repository.get_user(user_id=user_id)
        result = await self.users_repository.delete_user(user_id=user_id)

        return result
