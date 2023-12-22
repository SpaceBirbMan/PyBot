#TOKEN = '6543726409:AAHAdq7oWWnedQj6GlAd8KFLDVJubMZcKNk'
import re
import telepot
from telepot.loop import MessageLoop
from parsing import TParser
from selenium import webdriver

#схема работы бота, чтоб убедительно было
#комменты
#помощь
#кнопочки
#команды
#курс тенге
#курс доллара
#курс евро
#всё это через if
#закинуть класс бота в другой модуль
#проработать таймаут для выключения
#переделать парсер через beautifulsoup4

print("Бот запущен")
class ChatBot:
    def __init__(self):
        self.welcome_message = "Привет! Я ваш чат-бот. Как я могу помочь вам сегодня?"

    def _hello(self, user_input):
        hello_patterns = {
            r'\bпр.вет\b': 'привет',
            r'\bздр.(в)ствуй(те)?\b': 'здравствуйте',
            r'\bдобрый\sдень\b': 'добрый день',
            r'\bдобрый\sвеч.р\b': 'добрый вечер',
            r'\bдобр.е\sутр.\b': 'доброе утро',
            r'\bзд.ров.\b' : 'здорово'
        }
        for pattern, hello_text in hello_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return hello_text
        return None
    def is_goodbye(self, user_input):
        goodbye_patterns = {
            r'\bп.к.\b': 'пока',
            r'\bд.\sсв.дан.я\b': 'до свидания',
            r'\bпр.щай\b': 'прощай',
            r'\bдо\sскор.й\sвстреч.\b': 'до скорой встречи',
            r'\bвс..о\sдобр...\b': 'всего доброго',
            r'\bп.кед.\b': 'покеда'
        }

        for pattern, goodbye_text in goodbye_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return goodbye_text

        return None

    TPars = TParser("https://www.timeserver.ru/cities/ru/chita-zabaykalsky-krai")

    def need_time(self, user_input):
        need_time_patterns = [
            r'\bскажи\b\s*время\b',  # "скажи время"
            r'\bпокажи\b\s*время\b',  # "покажи время"
            r'\bвремя\b'  # "время"
        ]
        for pattern in need_time_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                #надо вывести, что бот думает
                self.TPars.driver = webdriver.Edge()
                return self.TPars.need_time()
        return None

    def respond(self, user_input):
        '''
        Генерирует ответ, в зависимости от условия
        :param user_input: текст сообщения пользователя
        :return: текст сообщения на вывод
        '''

        goodbye_text = self.is_goodbye(user_input)
        need_time_text = self.need_time(user_input)
        hello_text = self._hello(user_input)

        if hello_text:
            return f"{hello_text.capitalize()}! Я ваш чат-бот. Как я могу помочь вам сегодня?"
        if goodbye_text:
            return f"{goodbye_text.capitalize()}! Если у тебя будут еще вопросы, спрашивай."
        if need_time_text:
            self.TPars.driver.quit()
            return f"Текущее местное время " + need_time_text
        else:
            return "Бот: Это интересно! Я еще учусь и не могу обсуждать всё, но давай продолжим разговор."

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    user_input = msg['text']  # тут лежит текст сообщения

    if content_type == 'text':
        if user_input.lower() == '/start':
            response = "Привет! Я чат-бот. Как я могу помочь тебе сегодня?"
 #/time       
else:
            response = my_bot.respond(user_input)
        bot.sendMessage(chat_id, response)

def main():
    TOKEN = '6543726409:AAHAdq7oWWnedQj6GlAd8KFLDVJubMZcKNk'
    global bot  # Чтобы можно было использовать в других функциях
    bot = telepot.Bot(TOKEN)

    global my_bot #юзается выше
    my_bot = ChatBot()

    MessageLoop(bot, handle).run_as_thread()

    print("Бот готов к работе!")

    # Позволяет боту работать бесконечно
    while True:
        pass

if __name__ == '__main__':
    main()