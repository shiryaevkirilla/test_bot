import telebot
import webbrowser
from telebot import types
import sqlite3


bot = telebot.TeleBot('6129316486:AAFwKzsBYYbEMJpySLWBSCXQo3f6MLBE5d0')
name = None

def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')   # выводим сообещение
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Deleted photo')   # выводим сообещение


# получаем текст, который был введен пользователем
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    # выполняем регистрацию пользователей
    # подключаемся к файлу
    conn = sqlite3.connect('database.sql')
    # создаем курсор
    cur = conn.cursor()
    # выполняем команду
    # поле инкремент (авто-id) будет автоматически подставляться
    # '%s' - в это место будут подставлены данные
    # ... % (name, password) - будут подставлены такие данные, как name и password
    cur.execute(f"INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))  # позволяет выполнять sql-команды
    # выполняем синхронизацию
    conn.commit()
    # закрытие БД
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список зарегистрированных пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    # bot.register_next_step_handler(message, user_pass)

# принимает один параметр, который принимает одну функцию
# эта функция будет принимать один параметр, который будет возвращать значение True, если его не будет
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')  # позволяет выполнять sql-команды
    # conn.commit() - команду коммит прописывать не надо, т.к. она срабатывает для создания, добавления и удаления чего-либо из БД

    # вместо commit надо использовать функцию курсора - fetchall()
    users = cur.fetchall()   # эта функцию вернет все найденные записи

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    # тут вместо message.chat.id, ставим call.message.chat.id, тк работаем с call
    bot.send_message(call.message.chat.id, info)






# при комманде /start под клавиатурой будут появляться кнопки
@bot.message_handler(commands=['start'])
def start(message):
    # создание БД
    conn = sqlite3.connect('database.sql')
    # через курсор мы сможем выполнять различные программы, связанные с БД
    cur = conn.cursor()

    # создаем таблицу
    # команда execute - подготавливает sql-команду
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')   # позволяет выполнять sql-команды
    # функция commit синхронизирует все изменения и точно такая таблица будет у нас в файла БД
    conn.commit()
    # закрываем соединение с БД
    cur.close()
    # закрываем само соединение
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Введите ваше имя')

    # регистрируем следующую функцию
    bot.register_next_step_handler(message, user_name)


    # markup = types.ReplyKeyboardMarkup()  # встроенные кнопки
    #
    # # callback - означает, что при нажатии на эту кнопку будет вызываться некая функция
    # btn1 = types.KeyboardButton('Перейти на сайт😀')
    # markup.row(btn1)
    # btn2 = types.KeyboardButton('Удалить фото')
    # btn3 = types.KeyboardButton('Изменить текст')
    # markup.row(btn2, btn3)
    #
    # # отправляем пользователю изображение
    # file = open('./images/eng_photo.png', 'rb')   # rb - формат открытия, на чтение
    # bot.send_photo(message.chat.id, file, reply_markup=markup)
    #
    # # отсправляем пользователю песню
    # file = open('./audios/Rajda_Butylki.mp3', 'rb')  # rb - формат открытия, на чтение
    # bot.send_audio(message.chat.id, file, reply_markup=markup)
    #
    #
    #
    # # следующая функция, которая будет срабатывать при вводе любого тектса в чат
    # # будет срабатывать один раз и неважно что нажмет пользователь (кнопку 1, 2 или 3)
    # bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)




# @bot - декоратор для функции
# message_handler - обращаемся к такому декоратору как message_handlers
# commands - принимает те значения, которые мы будем обрабатывать
@bot.message_handler(commands=['main', 'hello'])
# как только будет вводиться команда /start, будет выполняться эта функция
# message - хранит в себе информацию про пользователя и чат
def main(message):
    # как только будет вводиться команда /start, мы будем отправлять пользователю "Привет!"
    # message.chat.id - получаю id чата
    # bot.send_message(message.chat.id, "Привет!")

    # вывод информации о пользователе, чате, тг-боте
    # bot.send_message(message.chat.id, message)

    if message.from_user.first_name == "annklubova":
        bot.send_message(message.chat.id, 'Рад вас поприветствовать, моя любимая Анечка!')
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')


@bot.message_handler(commands=['help'])
def main(message):
    # отформатированный текст
    bot.send_message(message.chat.id, '<b>Help</b> <em><u>information</u></em>', parse_mode='html')

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.youtube.com/watch?v=lbHGzZX85_s')


# обработаем обычный текст, который будет введен пользователем
# обработку обычного текста лучше располагать внизу, после обработки комманд
@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'id':
        # ответ на некое предыдущее сообщение
        bot.reply_to(message, f'ID: {message.from_user.id}')

@bot.message_handler(content_types=['photo'])
def get_photo(message):
    # создание кнопок
    markup = types.InlineKeyboardMarkup()   # встроенные кнопки

    # callback - означает, что при нажатии на эту кнопку будет вызываться некая функция
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.youtube.com/')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)

    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)


# декоратор, котораый обработывает callback_data
# в питоне анонимные функции - это лямбда-функции
@bot.callback_query_handler(func=lambda callback: True)   # у нас будет один параметр, если он будет пустым, то возврщается True
def callback_message(callback):
    # если пользователь жмет на кнопку delete, то отправляется callback_data с 'delete'
    if callback.data == 'delete':
        # delete_message - позволяет удалить сообщение
        # callback.message.chat.id - id чата
        # callback.message.message_id - id предпоследнего сообщения
        bot.delete_message(callback.message.chat.id, callback.message.message_id -1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

# программа будет работать бесконечно
bot.polling(none_stop=True)
# bot.infinity_polling()