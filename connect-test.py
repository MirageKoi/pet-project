import asyncio
import asyncpg


async def run():
    conn = await asyncpg.connect(
        user="postgres",
        password="pass",
        database="postgres",
        host="127.0.0.1",
        port="5432",
    )
    values = await conn.fetch("""SELECT * FROM users""")
    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
