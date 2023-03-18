import time
import telebot
from telebot import types
from DataUsers import users_
import config
import threading


conf = config.conf()                                            # тут есть переменные из config.json


API_TOKEN = conf.Tg_TOKEN                                       # достаем токен для бота тг

bot = telebot.TeleBot(API_TOKEN)

Users = users_()

@bot.message_handler(commands=['help', 'start'])                # если в сообщении /start /help выдолняется эта функция 
def send_welcome(message):                                      
    if(conf.print_messages):                                    # если сообщения включины выести его 
        print( '/start '+str(message.chat.id) )

    Users.add_user(name = message.chat.id)                      # проверяет есть ли такой пользователь и добавляет его если нужно
    
                                                                # выводим ответ
    bot.send_message(message.chat.id ,"Привет , можешь просто написать свой вопрос и gpt chat тебе ответит")
    
@bot.message_handler(commands=[ 'del'])
def send_welcome(message):
    
    Users.add_user(name = message.chat.id)
    Users.del_storeg(name = message.chat.id)
    
        
    bot.send_message(message.chat.id ,"del - ok" )
   
                                                                # срабатывает если приишло сообщение не /start /help 
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    Users.add_user(name = message.chat.id)                      # проверяет есть ли такой пользователь и добавляет его если нужно
    if(conf.print_messages):                                    # если сообщения включины выести его 
        print( str(message.chat.id) +' / '+'>> '+message.text)

    ret = Users.generate_response_user(message.chat.id, message.text)   # этот метод принимает айди чата и сообщения пользователя и позвращает ответ

    if(conf.print_messages):                                    # если сообщения включины выести его 
        print( str(message.chat.id) +' / '+'<< '+ret)

    try:                                                        #  parse_mode = "Markdown" позволяет красиво показывать код написанный сетью, но иногда выдает ошибку
        bot.send_message(message.chat.id ,str(ret), parse_mode = "Markdown" )
    except:
        bot.send_message(message.chat.id ,str(ret) )
    


def console():
    while True:
        mess = input(">> ")
        if len(mess):
            if mess[0] == "/":
                if mess == "/get_storeg":
                    i = 1
                    while i:
                        name = str(input("get_storeg >> name = "))
                        if name == "ex": break
                        for x in Users.musers:
                            if name == str(x.name):
                                i = 0
                                print("Storeg / ", name , x.storeg)
                if mess == "/users_len":
                    
                    print("users_len = ", len(Users.musers)) 


                if mess == "/code":
                    while True:
                        command = input("command >> ")
                        if command == "ex": break
                        try:
                            eval(command)                   
                        except Exception as e:
                            print("<< error: ", e)    
def console2():
    while True:
        command = input(">> ")
        try:
            eval(command)                   
        except Exception as e:
            print("<< error: ", e)

t = threading.Thread(target= console)                           # консоль для отладки 
t.start()

bot.infinity_polling()                                          # запуск бота 