from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import logging
import os
from telegram import Update,Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from db import *
# from scraper import scrape
from fetch_request import fetch
from qr import get_qr
from dotenv import load_dotenv
from datetime import date

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
today = date.today()

CONTACT, PASSWORD = range(2)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("👋 Welcome! Please enter your contact:")
    return CONTACT

async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("👍 Got it. Now enter your password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    contact = context.user_data["contact"]
    password = update.message.text
    username,user_id = await fetch(contact,password)

    await save_user_credentials(chat_id, contact, password, username, user_id)
    await update.message.reply_text("✅ Credentials saved! You'll get daily updates at 6 AM.")
    return ConversationHandler.END

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    creds = await get_user_credentials(chat_id)
    if creds:
        contact, password = creds
        await update.message.reply_text(
            f"🔑 Your saved credentials:\n👤 Username: {contact}\n🔒 Password: {password}"
        )
    else:
        await update.message.reply_text("⚠️ No credentials found. Use /start to set them.")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = Bot(token=BOT_TOKEN)
    chat_id = update.effective_chat.id
    creds = await get_user_credentials(chat_id)
    contact,password = creds
    user_id = await get_user_id(chat_id)
    if user_id:
        try:
            target_string = (f"{user_id}/{today}/student")
            image_path = await get_qr(target_string)

            if image_path:
                async with bot:
                    await bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"))
                    await update.message.reply_text(f"✅ Here is your image for {today} !")

                print(f"✅ Sent image to {contact}")
            else:
                print(f"⚠️ No image generated for {contact}")

        except Exception as e:
            print(f"❌ Failed to send to {contact}: {e}")

    else:
        await update.message.reply_text("❌ No credentials found. Please set them first.")



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END


async def scheduled_job():
    bot = Bot(token=BOT_TOKEN)
    users = await get_all_users()

    for user in users:
        chat_id = user["chat_id"]
        contact = user["contact"]
        password = user["password"]
        user_id = user["user_id"]
        try:
            target_string = (f"{user_id}/{today}/student")
            image_path = await get_qr(target_string)
            if image_path:
                async with bot:
                    await bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"))
                    await update.message.reply_text(f"✅ Here is your image for {today} !")

        except Exception as e:
            print(f"❌ Failed for {chat_id}: {e}")


def main():
    # 🔑 Create and set a new event loop for PTB
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("show", show))
    app.add_handler(CommandHandler("qr", send))

    scheduler = AsyncIOScheduler(event_loop=loop, timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_job, "cron", hour=6, minute=00)
    scheduler.start()


    print("🤖 Bot is running...")
    app.run_polling()   # now works with the manually set loop


if __name__ == "__main__":
    asyncio.run(init_db())  # run async DB init once
    main()