# db.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    await conn.close()

async def save_user_credentials(chat_id: int, username: str, password: str):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO users (chat_id, username, password)
        VALUES ($1, $2, $3)
        ON CONFLICT (chat_id) DO UPDATE
        SET username = EXCLUDED.username,
            password = EXCLUDED.password
    """, chat_id, username, password)
    await conn.close()

async def get_user_credentials(chat_id: int):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow(
            "SELECT username, password FROM users WHERE chat_id = $1",
            chat_id
        )
        if row:
            return row["username"], row["password"]
        return None
    finally:
        await conn.close()

async def get_all_users():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT chat_id, username, password FROM users")
    await conn.close()
    return [{'chat_id': r['chat_id'], 'username': r['username'], 'password': r['password']} for r in rows]
