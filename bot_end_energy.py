import telebot
import requests
from bs4 import BeautifulSoup
from Setting_bot import KeyInline

bot = telebot.TeleBot(KeyInline)
# бот создан для просмотра плановых отключений по Кировской области.
# Функция для получения информации с сайта
def fetch_data(url,text):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Извлечение данных из тегов <tr class="table-data">
        table_data = soup.find_all('tr', class_='table-data')
        extracted_data = []

        for row in table_data:
            cols = row.find_all('td')  # Получаем все ячейки в данной строке
            cols = [col.text.strip() for col in cols]  # Извлекаем текст и убираем лишние пробелы
            extracted_data.append(cols)  # Добавляем список ячеек в общий список

        data = []
        # Форматируем данные для вывода
        formatted_data = f"Table Data:\n"
        
        for idx, row in enumerate(extracted_data):
            # print(row)
            if row[1].lower().count(text.lower())>0:
                formatted_data += f"Row {idx + 1}: {', '.join(row)}\n"
                data.append(row)
        

        return data
    except Exception as e:
        return f"Ошибка при получении данных: {str(e)}"

# Обработчик инлайн-запросов
@bot.inline_handler(lambda query: len(query.query) > 10)
def inline(inline_query):
    
    text = inline_query.query[9:]
    if len(text)>0:
        data = fetch_data('https://xn--c1adoiagaegs3a5j.xn--p1ai/documents/planned-outage',text)
        
        
        if len(data)>0:
            text = 'По адресу '
            for lis in data:
                text += lis[2][:-1]+ '  будет отключение с '+ lis[3] + ' по ' + lis[4] + '\n'
            # Формирование результатов
            result = telebot.types.InlineQueryResultArticle(
                id=inline_query.id,
                title="Информация получена",
                input_message_content=telebot.types.InputTextMessageContent(text)
            )
        else:
            result = telebot.types.InlineQueryResultArticle(
                id=inline_query.id,
                title="Информация получена",
                input_message_content=telebot.types.InputTextMessageContent('Отключение не будет')
            )
    else:
        result = telebot.types.InlineQueryResultArticle(
                id=inline_query.id,
                title="Кокретизируйте ваш запрос",
                input_message_content=telebot.types.InputTextMessageContent(' ')
            )
    
    # Отправляем ответ пользователю
    bot.answer_inline_query(inline_query.id, [result])

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)