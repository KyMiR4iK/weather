import requests
import bs4

from dayWeather import DayWeather

class WeatherParser:

    def __init__(self): # Конструктор
        pass

    def prettify_temperature(self, temperature):
        _temperature = temperature.text
        _temperature = _temperature.replace('°', '').replace('\n', '').replace('\t', '')
        return int(_temperature)
    
    def prettify_date(self, date):
        _date = date.text
        _date = _date.strip().lower()
        _date = _date.replace('сегодня', '').strip()
        print(_date)
        return _date

    def parse_and_soup_page(self, web_page): # Спарсить страницу и сварить суп
        request_page = requests.get(web_page)
        soup = bs4.BeautifulSoup(request_page.text, "html5lib")

        return soup
    
    def get_date_for_moment_and_10_days(self, soup):
        date = soup.find('main', {'class' : ['d66a4e1abc', 'c05bc31d91', 'b19fe90d27']})
        date = date.findAll('div', {'class' : ['c3132db061', 'fd517a8fd5']})[1]
        date = date.text.replace(',', '').split()
        return date

    def get_soup_for_moment_and_10_days(self):
            return self.parse_and_soup_page("https://pogoda.mail.ru/prognoz/moskva/")

    def get_temperature_at_moment(self): # Температура на данный момент
        soup = self.get_soup_for_moment_and_10_days() # Получение супа
        soup = soup.find('div', {'class': ['e487206871', 'dedbbf63df', 'bfbd3eb239'],'data-qa': 'Title'}) # Получение блока с температурой
        
        return self.prettify_temperature(soup)
    
    def get_temperature_for_10_days(self): # Температура на 10 дней
        soup = self.get_soup_for_moment_and_10_days()
        year = self.get_date_for_moment_and_10_days(soup)[4]
        soup = soup.findAll('div', {'class' : ['swiper-wrapper']})[1] # Блок с погодой на 10 дней
        soup = soup.findAll('div', {'class' : ['swiper-slide']}) # Массив из 10 дней
        days = [self.create_dayWeeahter(day, year) for day in soup]
        
        return days
    
    def get_temperature_for_month(self, month, year):
        soup = self.parse_and_soup_page(f"https://pogoda.mail.ru/prognoz/moskva/{month}-{year}/")
        soup = soup.findAll('div', {'class' : ['day', 'day_calendar']})[1:] # Все строки календаря
        days = []
        for i in soup:
            if len(i.text) > 5:
                date = i.find('div', {'class' : 'day__date'})
                date = self.prettify_date(date)
                temperature = i.find('div', {'class' : 'day__temperature'}).contents[0]
                temperature = self.prettify_temperature(temperature)
                day = DayWeather(date, temperature)
                days.append(day)
        return days 
    
    def create_dayWeeahter(self, slide, year):
        date = slide.find('div', {'class' : ['e6255c6329']}).text + f' {year}'
        temperature = slide.find('div', {'class' : ['e487206871',  'a7b7a4c92f']}) # Берём температуру 
        temperature = self.prettify_temperature(temperature) # Делаем числом

        day = DayWeather(date, temperature)

        return day


         


