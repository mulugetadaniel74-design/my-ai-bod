import os
import telebot
from groq import Groq

# Variables የሚወሰዱት ከ Zeabur settings ላይ ነው
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! ቦቱ ዝግጁ ነው። ምን ላግዝህ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ጥያቄውን ወደ AI መላክ
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "አንተ ሁሉንም ነገር የምታውቅ፣ በአማርኛ እና በእንግሊዝኛ የምትመልስ ጎበዝ ረዳት ነህ።"},
                {"role": "user", "content": message.text}
            ]
        )
        # መልሱን ለተጠቃሚው መመለስ
        bot.reply_to(message, completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ ምላሽ መስጠት አልቻልኩም። እባክህ ቆይተህ ሞክር።")

if name == "main":
    print("ቦቱ መስራት ጀምሯል...")
    bot.polling(none_stop=True)
