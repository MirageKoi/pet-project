from dataclasses import dataclass
from typing import List

from asyncpg import Pool
from models.user import User, UserCreate


@dataclass
class UsersRepository:
    pool: Pool

    async def get_all_users(self) -> List[User]:
        async with self.pool.acquire() as connection:
            records = await connection.fetch("SELECT * FROM users")
            result = [User.model_validate(dict(record)) for record in records]
        return result

    async def get_user(self, user_id: int) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
            if not record:
                raise ValueError(f"User with id {user_id} does not exist")
        return User(**dict(record))

    async def create_user(self, new_user: UserCreate) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """INSERT INTO users (username, email, password_hash, password_salt) VALUES ($1, $2, $3, $4) RETURNING *""",
                new_user.username,
                new_user.email,
                new_user.password_hash,
                new_user.password_salt,
            )
            return User.model_validate(dict(record))

    async def update_user(self, item: User) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """UPDATE users SET username = $1, email = $2 WHERE user_id = $3 RETURNING *""",
                item.username,
                item.email,
                item.user_id,
            )
            return User.model_validate(dict(record))

    async def delete_user(self, user_id: int) -> bool:
        async with self.pool.acquire() as connection:
            value = await connection.execute("""DELETE FROM users WHERE user_id = $1""", user_id)
            return bool(value.split()[1])
