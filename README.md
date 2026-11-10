# 🤖 QSpiders Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-20.8-blue?logo=python)](https://github.com/python-telegram-bot/python-telegram-bot)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Telegram bot that authenticates QSpiders students, generates daily attendance QR codes, and automatically sends them to users every morning at 6 AM IST. Includes a FastAPI healthcheck endpoint for cloud deployment (Render, Railway, etc.).

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [License](#-license)
- [Contributing](#-contributing)

---

## ✨ Features

- 🔐 **Secure Login** — Users submit their QSpiders contact number and password via Telegram.
- 📅 **Daily Auto-Delivery** — A scheduler sends the day's attendance QR image to all registered users at 6 AM IST (Asia/Kolkata).
- 📸 **On-Demand QR** — Users can request their QR image anytime using the `/qr` command.
- 🔑 **Saved Credentials** — Credentials are stored in PostgreSQL and can be viewed with `/show`.
- 💚 **Healthcheck** — FastAPI `/` endpoint for uptime monitoring and cloud platform health checks.
- 🐳 **Docker Ready** — Dockerfile included for containerized deployment.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Bot Framework | python-telegram-bot (v20) |
| Scheduling | APScheduler (cron, Asia/Kolkata) |
| Database | PostgreSQL via asyncpg |
| Healthcheck API | FastAPI + Uvicorn |
| QR Generation | qrcode + Pillow |
| Env Config | python-dotenv |
| Container | Docker |
| Deployment | Render-compatible |

---

## 🧠 How It Works

1. A user starts the bot with `/start` and enters their QSpiders contact number and password.
2. The bot validates credentials against the QSpiders login API (`golive.qspiders.com`) and stores them (encrypted contact/password + user_id) in PostgreSQL, keyed by Telegram `chat_id`.
3. Every day at 6:00 AM IST, `APScheduler` triggers a job that:
   - Fetches all registered users.
   - Generates a QR code for `user_id/today/student`.
   - Sends the QR image to each user's chat.
4. Users can also request their QR on demand with `/qr`, or view saved credentials with `/show`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL database
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/qspider-telegram-bot.git
   cd qspider-telegram-bot
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

5. **Initialize the database**
   The `users` table is created automatically on first run via `init_db()`.

6. **Run the bot**
   ```bash
   python bot.py
   ```

   You should see `🤖 Bot is running...` in the console.

---

## 💻 Usage

| Command | Description |
|---------|-------------|
| `/start` | Begin registration — enter contact number and password |
| `/show` | View your saved credentials |
| `/qr` | Request today's attendance QR image on demand |
| `/cancel` | Cancel the current registration flow |

### Example flow
```
/start
👋 Welcome! Please enter your registered contact number:
> 9876543210
👍 Got it. Now enter your password:
> ********
✅ Credentials saved! You'll get daily updates at 6 AM.
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Telegram bot token from @BotFather |
| `DATABASE_URL` | Yes | PostgreSQL connection string |

---

## 🐳 Deployment

### Docker

Build and run the container:

```bash
docker build -t qspider-telegram-bot .
docker run -d \
  -e BOT_TOKEN=your_token \
  -e DATABASE_URL=your_db_url \
  -p 10000:10000 \
  qspider-telegram-bot
```

The `Dockerfile` runs both the FastAPI healthcheck (on `$PORT`, default `10000`) and the Telegram bot polling in the same container.

### Render.com

This project is configured for deployment on [Render](https://render.com):
- Create a **Web Service** from this repository.
- Set the build command: `pip install -r requirements.txt`
- Set the start command: `uvicorn healthcheck:app --host 0.0.0.0 --port $PORT & python bot.py`
- Add `BOT_TOKEN` and `DATABASE_URL` as environment variables.
- Use a Render PostgreSQL database for `DATABASE_URL`.

---

## 📁 Project Structure

```
qspider-telegram-bot/
├── bot.py                 # Main Telegram bot entry point
├── healthcheck.py         # FastAPI healthcheck endpoint
├── db.py                  # PostgreSQL helpers (asyncpg)
├── fetch_request.py       # QSpiders login API client
├── qr.py                  # QR code generator
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .env                   # Environment variables (create locally, not committed)
└── .gitignore
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo, open issues, and submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

This is a third-party utility and is not officially affiliated with QSpiders. Use at your own risk. Never share your credentials with untrusted parties. The authors are not responsible for any account issues arising from use of this bot.

---

## 🙌 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [FastAPI](https://fastapi.tiangolo.com/)
- [asyncpg](https://github.com/MagicStack/asyncpg)
- [APScheduler](https://apscheduler.readthedocs.io/)
- Open source community for tools and resources