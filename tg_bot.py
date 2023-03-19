import threading

import telebot

import config
from DataUsers import Users, User

conf = config.config()  # тут есть переменные из config.json
logger = conf.logger
# достаем токен для бота тг
bot = telebot.TeleBot(conf.Tg_TOKEN)

users = Users()


@bot.message_handler(commands=['help', 'start'])  # если в сообщении /start /help выдолняется эта функция
def send_welcome(message):
    if conf.print_messages:  # если сообщения включины выести его
        print('/start ' + str(message.chat.id))

    users.get_or_create(id=message.chat.id)  # проверяет есть ли такой пользователь и добавляет его если нужно

    # выводим ответ
    bot.send_message(
        message.chat.id,
        "Привет, можешь просто написать свой вопрос и gpt chat тебе ответит"
    )


@bot.message_handler(commands=['del'])
def send_welcome(message):
    usr = users.get_or_create(id=message.chat.id)
    usr.history.clear()
    bot.send_message(message.chat.id, "del - ok")


# срабатывает если пришло сообщение не /start /help
@bot.message_handler()
def echo_message(message: telebot.types.Message):
    usr: User = users.get_or_create(id=message.chat.id)
    if conf.print_messages:  # если сообщения включены - вывести его
        logger.info(f'{message.chat.id}\n>> {message.text}')

    try:
        ret = usr.send_message(message.text)
    except Exception as e:
        ret = 'Произошла неизвестная ошибка'
        logger.exception(e)

    if conf.print_messages:  # если сообщения включены - вывести его
        logger.info(f'{message.chat.id}\n<< {ret}')

    try:  # parse_mode = "Markdown" позволяет красиво показывать код написанный сетью, но иногда выдает ошибку
        bot.send_message(message.chat.id, str(ret), parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, str(ret))


def console():
    while True:
        mess = input(">> ")
        if not len(mess):
            continue
        if mess[0] != "/":
            continue
        if mess == "/get_storeg":
            i = 1
            while i:
                name = str(input("get_storeg >> name = "))
                if name == "ex": break
                for x in users.users:
                    if name == str(x.name):
                        i = 0
                        print("Storeg / ", name, x.history)
        if mess == "/users_len":
            print(f'users_len = {len(users.users)}')

        if mess == "/code":
            while True:
                command = input("command >> ")
                if command == "exit":
                    break
                try:
                    eval(command)
                except Exception as e:
                    logger.exception(e)


def console2():
    while True:
        command = input(">> ")
        try:
            eval(command)
        except Exception as e:
            logger.exception(e)


# t = threading.Thread(target=console)  # консоль для отладки
# t.start()

bot.infinity_polling()  # запуск бота
