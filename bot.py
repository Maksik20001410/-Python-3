import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)
    hello_world = ("Добро пожаловать в бота, создателем которого является Макс Сенкель. Для начала работы с ботом введите команду '/Привет'. После этого появятся кнопки для запросов боту. Ну а дальше всё проще простого). Балуйтесь)")
    bot.send_message(message.chat.id, hello_world)


@bot.message_handler(commands=['Привет'])
def welcome(message):
    user_id = message.from_user.id
    if user_id == 883993558:
        stick = open('Jopka.tgs', 'rb')
        bot.send_sticker(message.chat.id, stick)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Где Макс?")
        item2 = types.KeyboardButton("Как дела?")
        item3 = types.KeyboardButton("Фото")

        markup.add(item1, item2, item3)

        bot.send_message(message.chat.id, "Хеллоу, {0.first_name}, зацени жопку)\nЯ - <b>{1.first_name}</b>, бот, который создан, чтобы тебя развеселить(по крайней мере Макс на это сильно надеется).".format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def botik(message):
    if message.chat.type == 'private':
        if message.text == 'Где Макс?':

            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("Решаю ЦТ", callback_data='RCT')
            item2 = types.InlineKeyboardButton("Делаю д/з", callback_data='DZ')
            item3 = types.InlineKeyboardButton("Просто лежу", callback_data='SVP')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Если ты тут, значит Макс сейчас занят или просто психует и не заходит в ВК. Но ты не переживай, с ним в любом случае все хорошо. Он зайдет и сразу тебе отпишет. А ты чем занимаешься?', reply_markup=markup)
        if message.text == 'Фото':
            file_id = open("cherep.jpg", "rb")
            bot.send_photo(message.chat.id, file_id)
        elif message.text == 'Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Неплохо", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Отлично, а как твои дела, зайчик мой?', reply_markup=markup)
        elif message.text == 'Не знаю':
            bot.send_message(message.chat.id, 'Так не бывает. Все хорошо?')
        elif message.text == 'Да':
            bot.send_message(message.chat.id, 'Ну молодец. Но смотри, я слежу за тобой и передам все Максу. И если что, то ты получишь по заднице)')
        elif message.text == 'Ахах':
            bot.send_message(message.chat.id, 'Да-да. Так что лучше скажи мне что не так, и тогда я ему не расскажу)')
        else:
            bot.send_message(message.chat.id, 'Макс еще не придумал как ответить на это(')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и умничка)')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Что не так, кот?')
            elif call.data == 'RCT':
                bot.send_message(call.message.chat.id, 'Молодчинка. Тогда не отвлекаю)')
            elif call.data == 'DZ':
                bot.send_message(call.message.chat.id, 'Хорошо. Как сделаешь - отпиши, я скучаю.')
            elif call.data == 'SVP':
                bot.send_message(call.message.chat.id, 'Не скучай. Набери меня и я попробую тебя развлечь)')

    except Exception as e:
        print(repr(e))


'''Run'''
bot.polling(none_stop=True)