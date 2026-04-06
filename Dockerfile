# 1. Base image
FROM python:3.9-slim

# 2. GCC aur basic tools install karein
RUN apt-get update && apt-get install -y gcc libc6-dev && rm -rf /var/lib/apt/lists/*

# 3. Work directory
WORKDIR /app

# 4. Files copy karein
COPY . .

# 5. C file compile karein
RUN gcc bgmi.c -o bgmi -pthread -O3 && chmod +x bgmi

# 6. Flask aur pyTelegramBotAPI install karein (Yahan galti thi)
RUN pip install --no-cache-dir flask pyTelegramBotAPI

# 7. Bot start karein
CMD ["python3", "bot.py"]
