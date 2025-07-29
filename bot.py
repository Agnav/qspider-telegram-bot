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
from db import init_db, save_user_credentials,  get_user_credentials
from scraper import scrape
from dotenv import load_dotenv
from datetime import date

import asyncio
# asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
# logging.basicConfig(level=logging.DEBUG)



load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
today = date.today()

# Conversation states
USERNAME, PASSWORD = range(2)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text("👋 Welcome! Please enter your username:")
    return USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["username"] = update.message.text
    await update.message.reply_text("👍 Got it. Now enter your password:")
    return PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = context.user_data["username"]
    password = update.message.text

    await save_user_credentials(chat_id, username, password)
    await update.message.reply_text("✅ Credentials saved! You'll get daily updates at 6 AM.")
    return ConversationHandler.END

async def show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    creds = await get_user_credentials(chat_id)
    if creds:
        username, password = creds
        await update.message.reply_text(
            f"🔑 Your saved credentials:\n👤 Username: {username}\n🔒 Password: {password}"
        )
    else:
        await update.message.reply_text("⚠️ No credentials found. Use /start to set them.")


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = Bot(token=BOT_TOKEN)
    chat_id = update.effective_chat.id
    creds = await get_user_credentials(chat_id)
    if creds:
        username, password = creds
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

    else:
        await update.message.reply_text("❌ No credentials found. Please set them first.")



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelled.")
    return ConversationHandler.END

def main():
    # 🔑 Create and set a new event loop for PTB
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
            PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("show", show))
    app.add_handler(CommandHandler("img", send))


    print("🤖 Bot is running...")
    app.run_polling()   # now works with the manually set loop


if __name__ == "__main__":
    asyncio.run(init_db())  # run async DB init once
    main()