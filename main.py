import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Render መዝጊያ መከላከያ
app = Flask('')
@app.route('/')
def home(): return "DMK Wisdom Bot is Live!"
def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ቁልፎችን መውሰድ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# ቶከኑ መኖሩን ማረጋገጫ
if not BOT_TOKEN:
    print("Error: BOT_TOKEN is missing in Render Environment!")
else:
    bot = telebot.TeleBot(BOT_TOKEN)
    client = Groq(api_key=GROQ_API_KEY)

    SYSTEM_INSTRUCTION = (
        "Your name is DMK Wisdom Bot, created by Daniel Mulugeta. "
        "Respond in the language the user uses. Be helpful and direct."
    )

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "ሰላም! እኔ DMK Wisdom Bot ነኝ። በምን ላግዝህ?")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            completion = client.chat.get.completions.create(
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
    if BOT_TOKEN:
        print("Bot is starting...")
        bot.polling(none_stop=True)
        
