#TOKEN = '6543726409:AAHAdq7oWWnedQj6GlAd8KFLDVJubMZcKNk'
from chat_bot_root import ChatBot

import telepot
from telepot.loop import MessageLoop


'''
[клиент]<--[ответ]<-[обработка]
   |                     ^
   v                     |
[цикл]->[запрос]--->[класс бота]

'''

print("Бот запущен")



def handle(msg):
    '''
    Получает из мессенджера сообщение
    :param msg: введённое сообщение
    :return: ответ
    '''
    content_type, chat_type, chat_id = telepot.glance(msg)
    user_input = msg['text']  # тут лежит текст сообщения

    if content_type == 'text':
        if user_input.lower() == '/start':
            response = "Привет! Я чат-бот. Как я могу помочь тебе сегодня?"
        if user_input.lower() == '/help':
            response = ("Этот бот может:\n "
                        "Поздороваться\n "
                        "Попрощаться\n "
                        "Скажет курс валюты\n "
                        "Скажет местное время\n "
                        "Скажет пинг сети\n"
                        "Поработает с файлами (/json /txt /xlsx /csv)\n "
                        "Сгенерирует числа от а до b ([a,b])")
        else:
            if py_bot.get_req_id():
                wait_message = bot.sendMessage(chat_id, "Ожидайте, бот думает...")
                response = py_bot.respond(user_input)
                bot.deleteMessage((chat_id, wait_message['message_id']))
            else:
                response = py_bot.respond(user_input)
        bot.sendMessage(chat_id, response)
    py_bot.set_req_id(0)




def main():
    '''
    "Наружнее" пространство бота
    :return: ничего
    '''
    TOKEN = '6543726409:AAHAdq7oWWnedQj6GlAd8KFLDVJubMZcKNk'
    global bot  # Чтобы можно было использовать в других функциях
    bot = telepot.Bot(TOKEN)

    global py_bot #юзается выше
    py_bot = ChatBot()

    MessageLoop(bot, handle).run_as_thread()

    print("Бот готов к работе!")

    # Позволяет боту работать бесконечно
    while True:
        pass

if __name__ == '__main__':  # main не запустится, если этот файл куда-то подключить
    main()