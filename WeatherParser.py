import requests
import bs4

class WeatherParser:

    def __init__(self): # Конструктор
        pass

    def parse_and_soup_page(self, web_page): # Спарсить страницу и сварить суп
        request_page = requests.get(web_page)
        soup = bs4.BeautifulSoup(request_page.text, "html5lib")
        
        return soup
    
    def get_temperature_at_moment(self): # Температура на данный момент
        soup = self.parse_and_soup_page("https://pogoda.mail.ru/prognoz/moskva/") # Получение супа
        soup = soup.find('div', {'class': ['e487206871', 'dedbbf63df', 'bfbd3eb239'],'data-qa': 'Title'}) # Получение блока с температурой
        
        return self.prettify_temperature(soup)
    
    def get_temperature_for_10_days(self): # Температура на 10 дней
        pass

    def get_temperature_for_month(self):
        pass

    def prettify_temperature(self, temperature):
        return int(temperature.text.replace('°', ''))

