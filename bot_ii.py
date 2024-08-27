import telebot
from openai import OpenAI
from Setting_bot import SeyKeys, API_KEY

# Инициализация клиента OpenAI
client = OpenAI(
    api_key= API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

# Инициализация бота
bot = telebot.TeleBot(SeyKeys)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я ваш помощник-бот. Используйте команду /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Я умею отвечать на запросы с помощью ИИ")
    
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    messages = [
        {"role": "user", "content": message.text},
        {"role": "system", "content": "отвечай в стиле весёлого клоуна"}
    ]

    # Отправляем запрос к нейросети
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=messages
    )

    # Получаем ответ от нейросети
    assistant_response = chat_completion.choices[0].message.content
    
    # Отправляем ответ обратно в Telegram
    bot.reply_to(message, assistant_response)

# Запускаем бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling(none_stop=True)