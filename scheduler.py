import os
import asyncio
from db import get_all_users
from scraper import scrape
from telegram import Bot
from dotenv import load_dotenv
from datetime import date

today = date.today()
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    users = await get_all_users()

    for user in users:
        chat_id = user["chat_id"]
        username = user["username"]
        password = user["password"]

        try:
            image_path = await scrape(username, password, chat_id,)

            if image_path:
                async with bot:
                    await bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"), caption=f"Here is your image for {today} !")
                print(f"✅ Sent image to {username}")
            else:
                print(f"⚠️ No image generated for {username}")

        except Exception as e:
            print(f"❌ Failed to send to {username}: {e}")

if __name__ == "__main__":
    asyncio.run(main())
