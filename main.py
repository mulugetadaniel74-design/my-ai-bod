import os
import telebot
from groq import Groq

# ቁልፎችን ከ Render Environment እናመጣለን
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ማንነትህን የሚገልጽ መመሪያ
SYSTEM_INSTRUCTION = (
    "አንተ በዳንኤል ሙልጌታ (Daniel Mulugeta) የተሰራህ ትልቅ የቴክኖሎጂ ድርጅት ነህ። "
    "ስምህ 'DMK Wisdom Bot' ይባላል። ፈጣሪህ ዳንኤል ሙልጌታ (Tech Founder) ነው። "
    "ሁልጊዜ በአማርኛ ብቻ መልስ። ለተጠቃሚዎች ሰላምታ ስትሰጥ 'እኔ በዳንኤል ሙልጌታ የተሰራሁ የቴክኖሎጂ ድርጅት ነኝ' በል። "
    "እንግሊዝኛ አትጠቀም፣ በአጭርና ግልጽ አማርኛ ተናገር።"
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "ሰላም! እኔ በዳንኤል ሙልጌታ የተሰራሁ ትልቅ የቴክኖሎጂ ድርጅት ነኝ። ምን ላግዝህ?"
    bot.reply_to(message, welcome_text)

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

# ፎቶ ሲላክ እንዲያነብ (ለወደፊቱ Groq Vision ሲጨምር ዝግጁ ይሆናል)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "ፎቶውን አይቼዋለሁ! ነገር ግን በአሁኑ ሰዓት በጽሁፍ ብታወራኝ ይሻላል። እኔ በዳንኤል ሙልጌታ የተሰራሁ ረዳትህ ነኝ።")

bot.polling(none_stop=True)
