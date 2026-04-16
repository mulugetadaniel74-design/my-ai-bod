import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Render እንዳይዘጋ ፖርት መክፈቻ
app = Flask('')
@app.route('/')
def home(): return "DMK Wisdom Bot is Live!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ቁልፎች (ከ Render Environment የሚመጡ)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# የተሻሻለ መመሪያ (ቋንቋ እንዳይቀላቅል እና ቃላትን እንዳይደግም)
SYSTEM_INSTRUCTION = (
    "Your name is DMK Wisdom Bot, created by Daniel Mulugeta. "
    "Always respond in the same language the user uses. "
    "Do not repeat 'I am created by Daniel Mulugeta' in every message unless specifically asked. "
    "Be direct and helpful. If the user speaks Amharic, reply in Amharic. If English, reply in English."
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ DMK Wisdom Bot ነኝ። በምን ላግዝህ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.polling(none_stop=True)
        
