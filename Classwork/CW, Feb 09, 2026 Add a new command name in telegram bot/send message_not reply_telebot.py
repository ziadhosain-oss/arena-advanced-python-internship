import telebot

API_TOKEN = "8755115761:AAHQ_rpauieTwXtjKushG6IDKB3B8zO4ifU"

bot = telebot.TeleBot(API_TOKEN)

# /start and /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
   bot.reply_to(message, "Hello! How can I help you today?")

@bot.message_handler(commands=['help'])
def send_help(message):
   help_text = (
       "Here are the commands you can use:\n"
       "/start or /hello - Greet the bot\n"
       "/help - Show this help message\n"
       "/info - Get information about the bot"
   )
   bot.reply_to(message, help_text)

@bot.message_handler(commands=['info'])
def send_info(message):
   info_text = (
       "I am a simple Telegram bot created to demonstrate basic functionality.\n"
       "I can respond to commands and provide information about myself."
   )
   # bot.reply_to(message, info_text)
   bot.send_message(message.chat.id, info_text)




# Main loop
if __name__ == "__main__":
   print("Bot is running...")
   bot.polling()

