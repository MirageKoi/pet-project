from typing import List

from asyncpg import Pool
from models.user import User


class UsersRepository(object):
    def __init__(self, pool: Pool) -> None:
        self.pool = pool

    async def get_all_users(self) -> List[User]:
        async with self.pool.acquire() as connection:
            records = await connection.fetch("SELECT * FROM users")
            result = [User(**dict(q)) for q in records]
        return result

    async def get_user(self, user_id: int) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                "SELECT * FROM users WHERE user_id = $1", user_id
            )
            if not record:
                raise ValueError(f"User with id {user_id} does not exist")
        return User(**dict(record))

    async def create_user(self, email: str, age: int) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """INSERT INTO users (email, age) VALUES ($1, $2) RETURNING *""",
                email,
                age,
            )

            return User(**dict(record))

    async def update_user(self, user: User) -> User:
        async with self.pool.acquire() as connection:
            record = await connection.fetchrow(
                """UPDATE users SET email = COALESCE($1, email), age = COALESCE($2, age) WHERE user_id = $3 RETURNING *""",
                user.email,
                user.age,
                user.user_id,
            )
            return User(**dict(record))

    async def delete_user(self, user_id: int) -> bool:
        async with self.pool.acquire() as connection:
            value = await connection.execute(
                """DELETE FROM users WHERE user_id = $1""", user_id
            )
            return int(value.split()[1])
