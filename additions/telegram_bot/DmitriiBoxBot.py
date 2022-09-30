import telebot
from telebot import types

token = '5628898311:AAH25pZaEpTdCHodxxzuI9QhFu5JwFDCIhc'
bot = telebot.TeleBot(token)

# https://habr.com/ru/post/580408/

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['website'])
def website_message(message):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Кнопка", 'https://habr.com/ru/post/580408/')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    bot.send_message(message.chat.id, f"Привет {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['help'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, "<b> Yoooo </b>", parse_mode='html')
    elif message.text == 'Фото':
        photo = open('../game_1/static/game_1/img/rules.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

if __name__ == "__main__":
    # bot.infinity_polling()
    bot.polling(none_stop=True)