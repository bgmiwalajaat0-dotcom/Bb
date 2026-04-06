# 1. Base image set karein
FROM python:3.9-slim

# 2. System ko update karke GCC compiler install karein
RUN apt-get update && apt-get install -y gcc libc6-dev && rm -rf /var/lib/apt/lists/*

# 3. Working directory banayein
WORKDIR /app

# 4. Saari files copy karein
COPY . .

# 5. C file ko compile karein (RUN lagana zaroori hai)
RUN gcc bgmi.c -o bgmi -pthread -O3 && chmod +x bgmi

# 6. Python dependencies install karein
# Agar koi extra library hai toh yahan add karein, jaise:
RUN pip install --no-cache-dir pyTelegramBotAPI

# 7. Bot ko start karne ki command
CMD ["python3", "bot.py"]
