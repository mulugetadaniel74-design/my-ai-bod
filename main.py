import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Render የሚፈልገው ትንሽ የዌብ ሰርቨር
app = Flask('')

@app.route('/')
def home():
    return "ቦቱ በሰላም እየሰራ ነው!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# የቦት ዝግጅት
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_INSTRUCTION = (
    "አንተ በዳንኤል ሙልጌታ (Daniel Mulugeta) የተሰራህ ትልቅ የቴክኖሎጂ ድርጅት ነህ። "
    "ስምህ 'DMK Wisdom Bot' ይባላል። ፈጣሪህ ዳንኤል ሙልጌታ (Tech Founder) ነው። "
    "ሁልጊዜ በአጭርና ግልጽ አማርኛ ብቻ መልስ።"
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ በዳንኤል ሙልጌታ የተሰራሁ የቴክኖሎጂ ድርጅት ነኝ። ምን ላግዝህ?")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
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
    # ዌብ ሰርቨሩን በጎን ማስነሳት
    t = Thread(target=run_web)
    t.start()
    # ቦቱን ማስነሳት
    bot.polling(none_stop=True)
                 
