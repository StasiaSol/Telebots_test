import telebot
from openai import OpenAI
from Setting_bot import SeyKeys, API_KEY
from gtts import gTTS
import os
import requests

# Инициализация клиента OpenAI
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)
# Игровые данные
user_game_states = {}

# Инициализация бота
bot = telebot.TeleBot(SeyKeys)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Я ваш помощник-бот. Используйте команду /help, чтобы узнать, что я умею.")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Я умею отвечать на запросы с помощью ИИ и отправлять смешные картинки по команде /pint.\n"
                 "Чтобы начать игру, используйте команду /go.")

@bot.message_handler(commands=['pint'])
def send_funny_picture(message):
    # Получаем смешную картинку (например, кота)
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]['url']
        bot.send_photo(message.chat.id, image_url)
    else:
        bot.reply_to(message, "Извините, не удалось получить смешную картинку.")
        
@bot.message_handler(commands=['go'])
def start_game(message):
    user_game_states[message.chat.id] = {"character": None}
    bot.reply_to(message, "Выберите персонажа: 1. Воин 2. Маг 3. Лучник. Напишите номер вашего выбора.")

@bot.message_handler(func=lambda message: message.chat.id in user_game_states and user_game_states[message.chat.id]["character"] is None)
def choose_character(message):
    choice = message.text
    if choice == '1':
        user_game_states[message.chat.id]["character"] = "Воин"
        bot.reply_to(message, "Вы выбрали Воина! Готовьтесь к приключениям!")
    elif choice == '2':
        user_game_states[message.chat.id]["character"] = "Маг"
        bot.reply_to(message, "Вы выбрали Мага! Пора использовать заклинания!")
    elif choice == '3':
        user_game_states[message.chat.id]["character"] = "Лучник"
        bot.reply_to(message, "Вы выбрали Лучника! Время стрелять из лука!")
    else:
        bot.reply_to(message, "Пожалуйста, выберите 1, 2 или 3.")

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

    # Создаем голосовое сообщение
    tts = gTTS(text=assistant_response, lang='ru')
    audio_file = "response.mp3"
    tts.save(audio_file)

    # # Отправляем текстовый ответ обратно в Telegram
    # bot.reply_to(message, assistant_response)

    # Отправляем голосовое сообщение
    with open(audio_file, 'rb') as audio:
        bot.send_voice(message.chat.id, audio)

    # Удаляем временный аудиофайл
    os.remove(audio_file)

# Запускаем бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()