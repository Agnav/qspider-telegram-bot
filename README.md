# Telegram Scraper Bot

## Features

- Users submit credentials via Telegram
- Bot scrapes image daily at 6 AM
- Sends scraped image to each user

## How to Use

1. Add your bot token in `.env`
2. Run `bot.py` to accept user credentials
3. Scheduler will automatically run `scheduler.py` daily at 6 AM (UTC)

## Deployment

Supports [Render.com](https://render.com)

- Bot runs as a service
- `scheduler.py` runs as a daily cron job