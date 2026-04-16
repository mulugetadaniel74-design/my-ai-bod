import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# Render ላይ ቦቱ እንዳይዘጋ ፖርት መክፈቻ
app = Flask('')

@app.route('/')
def home():
    return "DMK Wisdom Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ቁልፎች
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ሁሉንም ቋንቋ እንዲችል የተደረገ መመሪያ
SYSTEM_INSTRUCTION = (
    "አንተ በዳንኤል ሙልጌታ (Daniel Mulugeta) የተሰራህ ትልቅ የቴክኖሎጂ ድርጅት ነህ። "
    "ስምህ 'DMK Wisdom Bot' ይባላል። ፈጣሪህ ዳንኤል ሙልጌታ (Tech Founder) ነው። "
    "ተጠቃሚው በየትኛውም ቋንቋ ቢጠይቅህ በዛው ቋንቋ በትህትና መልስ። "
    "ማን እንደሰራህ ከተጠየቅህ ግን ሁልጊዜ 'በዳንኤል ሙልጌታ የተሰራሁ ድርጅት ነኝ' በል።"
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ በዳንኤል ሙልጌታ የተሰራሁ የቴክኖሎጂ ድርጅት ነኝ። በፈለጉት ቋንቋ መጠየቅ ይችላሉ።")

# ፋይሎች ሲላኩ (ቮይስ፣ ቪዲዮ፣ ፎቶ)
@bot.message_handler(content_types=['photo', 'video', 'voice', 'document'])
def handle_files(message):
    msg = "ይህንን ፋይል አይቼዋለሁ! እኔ በዳንኤል ሙልጌታ የተሰራሁ የቴክኖሎጂ ድርጅት ነኝ። "
    msg += "ፈጣሪዬ ዳንኤል ለወደፊቱ ይህንን ፋይል እንድተነትን ያደርገኛል። ለአሁኑ ግን በጽሁፍ ያውሩኝ።"
    bot.reply_to(message, msg)

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
    t = Thread(target=run_web)
    t.start()
    print("ቦቱ መስራት ጀምሯል...")
    bot.polling(none_stop=True)
            
