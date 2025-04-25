import requests
import bs4

class WeatherParser:

    def __init__(self): # Конструктор
        self.web_page = "https://pogoda.mail.ru/prognoz/moskva/" # Сайт для парсинга.

    def parse_page(self): # Спарсить страницу и сварить суп
        request_page = requests.get(self.web_page)
        soup = bs4.BeautifulSoup(request_page.text)
        return soup
    
    def get_temperature(self, souped_page): # Достать температуру из супа
        pass

    def choose_option(self): # Меню выбора действий
        pass

    def save_data(self): # Сохранить температуру
        pass

    def show_data(self): # Показать сохранённую температуру
        pass


