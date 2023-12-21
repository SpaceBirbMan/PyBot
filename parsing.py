from bs4 import BeautifulSoup
import requests

class Parser:
    '''
    Класс парсера сайтов
    '''
    __url = ""  # адрес сайта
    __html_name = ""  # для работы с html
    __html_class = ""


    def __init__(self, url, html_name, html_class):
        '''
        Инициализация парсера
        :param url: адрес
        :param html_name: где искать
        :param html_class: что искать
        '''
        self.__url = url
        self.__html_class = html_class
        self.__html_name = html_name

    def get_info(self):
        '''
        Получает инфу по заданным данным
        :return: данные
        '''
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(self.__html_name, class_=self.__html_class)
        return element.text.strip()

    def get_row_from_table(self):
        '''
        Работает с табличкой, получает её строку по заданному "адресу"
        :return: данные
        '''
        response = requests.get(self.__url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find(self.__html_name, self.__html_class)