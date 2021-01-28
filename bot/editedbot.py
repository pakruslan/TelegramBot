from telebot import TeleBot, types
import csv
import parsing



token = '1408562148:AAEkA7Oad6JbP-gdVPduuR4FqQlk3E6FLfg'
bot = TeleBot(token)


get_data = []
number = 0


main_keyboard = types.InlineKeyboardMarkup(row_width=2)
btn1 = types.InlineKeyboardButton('Последние новости', callback_data="news")
btn2 = types.InlineKeyboardButton('Выйти', callback_data="quit")
main_keyboard.add(btn1, btn2)



@bot.message_handler(commands=['start'])
def start(msg):
    chat_id = msg.chat.id
    parsing.parse_main_page()
    bot.send_message(chat_id, 'Привет! Я новостной бот. Чем могу помочь?', reply_markup=main_keyboard)


@bot.callback_query_handler(func=lambda x: True)
def callback(x):
    chat_id = x.message.chat.id
    mes_id = x.message.message_id
    
    if x.data == 'news':
        with open(file="/home/emina/Documents/bootcamp/Hackathon/newnews.csv", mode='r') as file:
            global get_data
            content = file.readlines()
            new_list = []
            num = 0
            for i in content:
                num += 1
                get_title = i[0:i.index("h")]
                get_data.append(get_title)
                new_list.append(f'{num}. {get_title}\n')

        mes = bot.send_message(chat_id, ''.join(new_list[0:20]))
        msg = bot.send_message(chat_id, 'Выберите новостной номер')
        bot.register_next_step_handler(msg, get_num)
    elif x.data == 'quit':
        msg = bot.send_message(chat_id, 'До свидания')
    
def get_num(msg):
    global number
    chat_id = msg.chat.id
    number = msg.text
    send_title = get_data[int(number)-1] 
    descr_kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btn3 = types.KeyboardButton('Подробнее')
    descr_kb.add(btn3) 
    msg = bot.send_message(chat_id, send_title, reply_markup=descr_kb)
    bot.register_next_step_handler(msg, get_descr)
    

def get_descr(msg):
    chat_id = msg.chat.id
    parsing.parse_title_page(number)
    send_descr = parsing.call_descr()
    bot.send_message(chat_id, send_descr, reply_markup=main_keyboard)




bot.polling()