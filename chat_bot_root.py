import re
from parsing import Parser
import random
from ping3 import ping, verbose_ping
import json


class ChatBot:
    '''
    Класс бота и его методов
    '''

    '''
    Рабочие переменные
    '''
    __request_id: int = 0                                           # id запроса (сугубо для красоты при выводе)
    __work_with_multifunction = False                               # статус работы в блоке функций
    __json = None                                                   # переменная, хранящая json файл
    __status = "none"                                               # указывает на блок мультикоманд
    __reading_mode = False                                          # режим чтения для файлов
    __data = []                                                     # регистр для всяких данных

    def set_req_id(self, r_id):  # задаёт id запроса
        self.__request_id = r_id

    def get_req_id(self):  # выадаёт id запроса
        return self.__request_id

    def __init__(self):
        '''
        Создаёт самого бота
        '''
        self.welcome_message = "Привет! Я ваш чат-бот. Как я могу помочь вам сегодня?"

    def _hello(self, user_input):
        '''
        Приветствие
        :param user_input: текст с мессенджера
        :return: часть ответа бота
        '''
        self.set_req_id(1)
        hello_patterns = {
            r'\bпр.вет\b': 'привет',
            r'\bздр.(в)ствуй(те)?\b': 'здравствуйте',
            r'\bдобрый\sдень\b': 'добрый день',
            r'\bдобрый\sвеч.р\b': 'добрый вечер',
            r'\bдобр.е\sутр.\b': 'доброе утро',
            r'\bзд.ров.\b': 'здорово'
        }
        for pattern, hello_text in hello_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                return hello_text
        return None
    def is_goodbye(self, user_input):
        '''
        Прощание
        :param user_input: текст с мессенджера
        :return: часть ответа бота
        '''
        self.set_req_id(1)
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
    def need_valuta(self, user_input):
        '''
        Запрос валюты
        :param user_input: текст с мессенджера
        :return: факт срабатывания
        '''
        self.set_req_id(2)

        need_valuta_patterns = {
            r'\bв.лют.\b'
        }

        for pattern in need_valuta_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return True  #пачо мне тут текст выводить? Это ж запрос, пусть истина-ложь выводит
        return False

    def set_valuta(self, user_input):
        '''
        Вторая часть работы с валютой
        :param user_input: текст с мессенджера с информацией о валюте
        :return: Индекс запроса
        '''
        set_valuta_patterns = [
            r'\bлюб(?:ая|ое|ую|ой)\b',
            r'\busd\b',
            r'\beuro\b',
            r'\bдол[лл]ар[ыи]?\b',
            r'\bзел.нь\b',
            r'\bз.л(?:е|ё)н..\b',
            r'\bевр(?:о|а|ы|е)\b',
            r'\bт(?:е|ы|и|э)нг(?:е|ы|и|э)'
        ]

        index = 1
        for pattern in set_valuta_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                    return index
            index += 1
        return 0

    def get_valuta(self, icode):
        '''
        Третья и последня часть работы с валютой
        :param icode: индекс запроса
        :return: Данные о валюте
        '''
        code = ""
        if icode == 1:
            code = random.choice(['USD', 'EUR', 'KZT'])
        elif 2 <= icode <= 6:
            code = 'USD'
        elif icode == 3 or icode == 7:
            code = 'EUR'
        elif icode == 8:
            code = 'KZT'
        else:
            return "Похоже, вы ввели неверную валюту. Команда сброшена."
        val_pars = Parser("https://www.banki.ru/products/currency/cb/", 'tr', {'data-currency-code': code})

        pre_rate = val_pars.get_row_from_table()
        currency_code = pre_rate['data-currency-code']  # Получаем код валюты
        rate = f"{currency_code} {pre_rate.find('td', string=True, recursive=False).find_next('td').find_next('td').text.strip()}"
        return rate
    def need_time(self, user_input):
        '''
        Показывает время по запросу
        :param user_input: запрос времени с мессенджера
        :return: данные о времени
        '''
        self.set_req_id(2)
        need_time_patterns = {
            r'\bвремя\b'
        }
        tpars = Parser("https://www.timeserver.ru/cities/ru/chita-zabaykalsky-krai", "div", "timeview-data")
        for pattern in need_time_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return tpars.get_info()

        return None

    def need_ping(self, user_input):
        '''
        Выводит пинг по запросу
        :param user_input: Запрос с мессенджера
        :return: пинг в миллисекундах (только с ним не так что-то)
        '''
        self.set_req_id(2)
        need_ping_patterns = {
            r'\bпинг\b',
            r'\bping\b'
        }

        for pattern in need_ping_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                result = self.get_ping("m.vk.com")
                return result
        return None

    def get_ping(self, host):
        '''
        Замеряет пинг
        :param host: Сайт, с которым проводятся замеры
        :return: Пинг
        '''

        result = ping(host)
        if result is not None:
            ping_output = f"{result} мс"
            return ping_output
        else:
            return "Не удалось измерить пинг."

    def cmd_file(self, user_input):
        '''
        Получает запрос и устанавливает нужные флаги для последующей работы в блоке функций
        :param user_input: запрос
        :return: режим работы
        '''

        if user_input.lower() == '/json':
            self.__status = "json"
            return "JSON"
        if user_input.lower() == '/txt':
            self.__status = "txt"
            return "TXT"
        if user_input.lower() == '/xlsx':
            self.__status = "xlsx"
            return "XLSX"
        if user_input.lower() == '/csv':
            self.__status = "csv"
            return "CVS"
        return None

    def open_json(self, file_path):
        self.set_req_id(1)
        try:
            self.__json = open(file_path, 'a+', encoding='utf-8')
        except FileNotFoundError:
            # Если файл не существует, создаем новый
            self.__json = open(file_path, 'w+', encoding='utf-8')


    def dump_into_json(self, user_input):
        self.set_req_id(2)
        json.dump(user_input, self.__json, ensure_ascii=False, indent=2)

    def pull_form_json(self):
        self.set_req_id(1)
        self.__json.seek(0)  # Перемещаем указатель в начало файла
        data = self.__json.read()
        tmp = json.loads(data)
        return tmp

    def close_json(self):
        self.__json.close()
        self.__status = ""
        self.__work_with_multifunction = False
        self.__json = None

    def need_numbers(self, user_input):
        '''
        Получает запрос на вывод случайного числа
        :param user_input: Запрос
        :return: Список из двух чисел
        '''
        self.set_req_id(2)
        pattern = r'(-?\d+(\.\d+)?)\s*\,\s*(-?\d+(\.\d+)?)'
        if re.search(r'\[' + pattern + r'\]', user_input):
            match = re.search(pattern, user_input)
            if match:
                a = float(match[1])
                b = float(match[3])
                return [a, b]

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
        valuta_bool = self.need_valuta(user_input)
        nping = self.need_ping(user_input)
        self.cmd_file(user_input)
        nums = self.need_numbers(user_input)
        f_mode = self.cmd_file(user_input)

        file_cmd_patterns = [r'/открыть', r'/закрыть', r'/записать', r'/выгрузить']



        if not self.__work_with_multifunction:
            if hello_text:
                return f"{hello_text.capitalize()}! Я ваш чат-бот. Как я могу помочь вам сегодня?"
            if goodbye_text:
                return f"{goodbye_text.capitalize()}! Если у тебя будут еще вопросы, спрашивай."
            if nping:
                return f"Текущий пинг сети (m.vk.com)\n" + nping
            if need_time_text:
                return f"Текущее местное время " + need_time_text
            if nums:
                if nums[0] > nums[1]:
                    tmp = nums[1]
                    nums[1] = nums[0]
                    nums[0] = tmp
                rand = random.uniform(nums[0], nums[1]+1)
                return f"{rand}"
            if valuta_bool:
                self.__work_with_multifunction = True
                self.__status = "valuta"
                return f"Конечно! Выберите валюту (доллары, евро или тенге)"
            if f_mode:
                self.__work_with_multifunction = True
                return f"Запущена работа с файлами\nИспользуйте команды \n/открыть, \n/закрыть, \n/выгрузить \n/записать \nРежим: " + f_mode
            else:
                return "Бот: Это интересно! Я еще учусь и не могу обсуждать всё, но давай продолжим разговор."
        else:
            match self.__status:
                case "valuta":
                    icode = self.set_valuta(user_input)
                    self.__status = ""
                    self.__work_with_multifunction = False
                    return f"{self.get_valuta(icode)}"
                case "json":
                    if re.findall(user_input, file_cmd_patterns[0], re.IGNORECASE) and not self.__reading_mode:
                        self.open_json('bot_json')
                        return "JSON открыт"
                    elif re.findall(user_input, file_cmd_patterns[1], re.IGNORECASE):
                        self.dump_into_json(self.__data)
                        self.close_json()
                        self.__reading_mode = False
                        return f"JSON закрыт, режим чтения выключен, режим мультикоманд выключен"
                    elif re.findall(user_input, file_cmd_patterns[2], re.IGNORECASE):
                        self.__reading_mode = True
                        return "Запущен режим чтения, для выключения используйте команду \n/закрыть"
                    elif re.findall(user_input, file_cmd_patterns[3], re.IGNORECASE):
                        self.__reading_mode = False
                        return self.pull_form_json()
                    elif self.__reading_mode:
                        self.__data.append(user_input)
                        return "Записано"
                    else:
                        return "Ошибка ввода"
                case "txt":
                    a = None
                case "xlsx":
                    a = None
                case "csv":
                    a = None
