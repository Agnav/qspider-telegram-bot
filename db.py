# db.py
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL, ssl="require")
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id BIGINT PRIMARY KEY,
            contact TEXT,
            password TEXT,
            username TEXT,
            user_id BIGINT
        )
    """)
    await conn.close()

async def save_user_credentials(chat_id: int, contact: str, password: str, username:str, user_id: int):
    conn = await asyncpg.connect(DATABASE_URL, ssl="require")
    await conn.execute("""
        INSERT INTO users (chat_id, contact, password, username, user_id)
        VALUES ($1, $2, $3, $4, $5)
        ON CONFLICT (chat_id) DO UPDATE
        SET contact = EXCLUDED.contact,
            password = EXCLUDED.password,
            username = EXCLUDED.username,
            user_id = EXCLUDED.user_id
    """, chat_id, contact, password, username, user_id)
    await conn.close()

async def get_user_credentials(chat_id: int):
    conn = await asyncpg.connect(DATABASE_URL, ssl="require")
    try:
        row = await conn.fetchrow(
            "SELECT contact, password FROM users WHERE chat_id = $1",
            chat_id
        )
        if row:
            return row["contact"], row["password"]
        return None
    finally:
        await conn.close()


async def get_user_id(chat_id: int):
        conn = await asyncpg.connect(DATABASE_URL, ssl="require")
        try:
            row = await conn.fetchrow(
                "SELECT user_id FROM users WHERE chat_id = $1",
                chat_id
            )
            if row:
                return row["user_id"]
            return None
        finally:
            await conn.close()


async def get_all_users():
    conn = await asyncpg.connect(DATABASE_URL, ssl="require")
    rows = await conn.fetch("SELECT chat_id, contact, password user_id FROM users")
    await conn.close()
    return [{'chat_id': r['chat_id'], 'contact': r['contact'], 'password': r['password'], 'user_id': r['user_id']} for r in rows]
