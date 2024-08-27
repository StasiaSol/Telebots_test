from openai import OpenAI
from Setting_bot import API_KEY

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


def chat_with_ai():
    print("Добро пожаловать в чат с ИИ! Введите 'выход' для завершения.")
    
    # Начинаем с пустого списка сообщений
    messages = []

    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() == 'выход':
            print("Завершение чата.")
            break
        
        # Добавляем сообщение пользователя в список
        messages.append({"role": "user", "content": user_input})

        # Отправляем запрос к нейросети
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )

        # Получаем ответ от нейросети
        assistant_response = chat_completion.choices[0].message.content
        
        # Добавление ответа нейросети в список сообщений для контекста
        messages.append({"role": "system", "content": "отвечай в стиле весёлого клоуна"})

        # Выводим ответ ИИ
        print("ИИ:", assistant_response)

# Запускаем функцию чата
if __name__ == "__main__":
    chat_with_ai()
    
    