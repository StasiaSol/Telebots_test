import Setting_bot
import telebot
from telebot import types
import math

class Corn:
    def __init__(self):
        self.corner = 0

corn = Corn()
bot = telebot.TeleBot(Setting_bot.SeyKeys)
flag = ''

@bot.message_handler(commands = ['start'])
def start_message(message):
    
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='7', callback_data='7')
    button2 = types.InlineKeyboardButton(text='8', callback_data='8')
    button3 = types.InlineKeyboardButton(text='9', callback_data='9')
    button4 = types.InlineKeyboardButton(text='x', callback_data='x')
    keyboard.add(button1,button2,button3,button4)
    
    bot.send_message(message.chat.id, 'Калькулятор', 
                     reply_markup=keyboard)
    
@bot.callback_query_handler(lambda call:True)
def buttons(call):
    global flag
    if call.data == 'Sin':
        flag = 'Sin'
        bot.send_message(call.message.chat.id, f'Синус = {corn.corner}')
    elif call.data == 'Cos':
        flag = 'Cos'
        bot.send_message(call.message.chat.id, f'Косинус = {corn.corner}')
    elif call.data == 'Tan':
        flag = 'Tan'
        bot.send_message(call.message.chat.id, f'Тангентс = {corn.corner}')

@bot.message_handler(content_types = ['text'])
def repeat(message):
    global flag
    if (flag == 'Sin' and message.text != ''):
        corn.corner = math.sin(float(message.text)*math.pi/180)
        print(float(message.text)*math.pi/180)
        flag = ''
    elif (flag == 'Cos'  and message.text != ''):
        corn.corner = math.cos(float(message.text)*math.pi/180)
        print(corn.corner)
        flag = ''
    elif (flag == 'Tan'  and message.text != ''):
        corn.corner = math.tan(float(message.text)*math.pi/180)
        print(corn.corner)
        flag = ''
    
    

bot.polling(non_stop=True)
