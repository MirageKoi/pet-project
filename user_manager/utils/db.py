import asyncpg
from asyncpg import Pool


async def init_db(config: dict[str, str]) -> Pool:
    """Initialize a connection pool."""
    return await asyncpg.create_pool(
        user="postgres",
        password="pass",
        database="postgres",
        host="127.0.0.1",
        port="5432",
    )
