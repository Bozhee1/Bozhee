import telebot
import time
from telebot import types

TOKEN = '7166723464:AAHAF9UW3NetKN9c9SwQbvWSzxaoyV-Lcvc'
bot = telebot.TeleBot(TOKEN)


active_users = {}

def send_promo_code(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Воспользуюсь промокодом", callback_data='use_promo')
    item2 = types.InlineKeyboardButton("Не сегодня", callback_data='not_today')
    markup.add(item1, item2)
    
    bot.send_message(chat_id, "Понимаю, на обдумывание такого классного предложения нужно время. Чтобы это решение далось чуть быстрее, я дарю промокод «bozhee 20» со скидкой 20% на первый заказ бота или инфографики в течение суток 🔥", reply_markup=markup)


@bot.message_handler(content_types=['photo', 'GIF', 'video', 'voice', 'document'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Удалить файл?', callback_data='delete')
    markup.row(button1)
    bot.reply_to(message, 'Извините, но работу с фотографиями, аудио и видео разработчик в меня не добавлял:(', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1)


def handle_start(message, send_greeting=True):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("🟣 О разработчике 🙋🏼‍♂️")
    item2 = types.KeyboardButton("Для чего я был создан 🤖")
    item3 = types.KeyboardButton("Помощь в командах 🕵🏼‍♂️")
    item4 = types.KeyboardButton("Портфолио 💼")
    item5 = types.KeyboardButton("Связь 🤙🏻")
    markup.add(item1, item2, item3, item4, item5)
    
    if send_greeting:
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Выберите интересующий вас пункт меню:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def handle_start_command(message):
    handle_start(message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
 
    active_users[message.chat.id] = time.time()
    
    if message.text == "🟣 О разработчике 🙋🏼‍♂️":
        bot.send_message(message.chat.id, '''
🙋🏼‍♂️Меня зовут Артем, я профессионально изучаю программирование на языке Python и могу создать tg-ботов разной сложности.
🖼️ Также занимаюсь дизайном креативов в Photoshop (баннеры, карточки товара, визитки и т.д.) и базовым монтажом видео.
👇🏻О моих hard и soft skills 👇🏻
''')
        
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        item1 = types.KeyboardButton("▫️Навыки")
        item2 = types.KeyboardButton("▫️Качества")
        item3 = types.KeyboardButton("Вернуться")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Выберите интересующую вас информацию:", reply_markup=markup)
        
    elif message.text == "Связь 🤙🏻":
        bot.reply_to(message, '''
Мой тг: @Gosp0dispasi
Inst: https://www.instagram.com/_bozhee/
Kwork: https://kwork.ru/user/bozhee
''')
    elif message.text == "Портфолио 💼":
        bot.reply_to(message, ''' 
Мой опыт на данный момент небольшой, именно поэтому я делаю старательно и недорого для вас. 

🤖Кейс по созданию tg-ботов вы видите уже сейчас, проходя его.

🖼️Портфолио по креативам можно смотреть на моем профиле в kwork (ссылка на кворк)
''')
        
        
    elif message.text == "Для чего я был создан 🤖":
        bot.reply_to(message, "Я был создан разработчиком Bozhee, чтобы показать его возможности по разработке средних ботов")
    elif message.text == "Помощь в командах 🕵🏼‍♂️":
        bot.reply_to(message, "/start, остальные команды были сделаны в виде кнопок!")
    elif message.text == "▫️Навыки":
        bot.reply_to(message, '''— Знание языка программирования Питона    
— Умение работать в фш
— Монтаж видеороликов средней сложности''')
        
        
    elif message.text == "▫️Качества":
        bot.reply_to(message, '''
— Пунктуален (ставлю реальные сроки и укладываюсь в дедлайны)
— Насмотренность (сделаю стильно и дорого)
— Внимателен (вношу изменения до 10 бесплатных правок)
— Усидчив (всегда довожу до конца)
— Надежен (как швейцарские часы)
— Настроен на долгосрочное сотрудничество 
''')
        
        
    elif message.text == "Вернуться":
        handle_start(message, send_greeting=False)  

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'use_promo':
        bot.send_message(call.message.chat.id, "Держи промокодик")
    elif call.data == 'not_today':
        bot.send_message(call.message.chat.id, "Ждем твоих пожеланий в будущем.")

def check_inactive_user():
    while True:
        time.sleep(600)  # 10 минут
        current_time = time.time()
       
        for chat_id in active_users.copy():  
            last_active_time = active_users[chat_id]
            if current_time - last_active_time >= 600:
                send_promo_code(chat_id)
                del active_users[chat_id] 


import threading
threading.Thread(target=check_inactive_user, daemon=True).start()

bot.polling()
