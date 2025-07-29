FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set env var so selenium knows where Chromium is
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/bin:$PATH"

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

CMD ["python", "bot.py"]
