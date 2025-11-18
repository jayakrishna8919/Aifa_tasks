import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/test_db")

async def main():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY, name VARCHAR)"))
        await conn.execute(text("INSERT INTO users(name) VALUES ('Async User')"))
        result = await conn.execute(text("SELECT * FROM users"))
        rows = result.fetchall()
        print(rows)

asyncio.run(main())
