import requests
import bs4
from weatherParserError import WeatherParserError
from dayWeather import DayWeather

class WeatherParser:
    BASE_URL = "https://pogoda.mail.ru/prognoz/moskva/"
    REQUEST_TIMEOUT = 10
    SELECTORS = {
        'current_temp': {'class': ['e487206871', 'dedbbf63df', 'bfbd3eb239'], 'data-qa': 'Title'},
        '10day_wrapper': {'class': ['swiper-wrapper']},
        'date_block': {'class': ['c3132db061', 'fd517a8fd5']},
        'day_slide': {'class': ['swiper-slide']},
        'calendar_day': {'class': ['day', 'day_calendar']}
    }

    def __init__(self):
        self.session = requests.Session()

    def prettify_temperature(self, temperature):
        try:
            _temperature = temperature.text
            _temperature = _temperature.replace('°', '').replace('\n', '').replace('\t', '')
            return int(_temperature)
        except (AttributeError, ValueError) as e:
            raise WeatherParserError(f"Ошибка обработки температуры: {e}")

    def prettify_date(self, date):
        try:
            _date = date.text
            _date = _date.strip().lower()
            _date = _date.replace('сегодня', '').strip()
            return _date
        except AttributeError as e:
            raise WeatherParserError(f"Ошибка обработки даты: {e}")

    def parse_and_soup_page(self, web_page):
        try:
            request_page = self.session.get(
                web_page,
                timeout=self.REQUEST_TIMEOUT
            )
            request_page.raise_for_status()
            return bs4.BeautifulSoup(request_page.text, "html.parser")
        except requests.exceptions.RequestException as e:
            raise WeatherParserError(f"Ошибка при запросе страницы: {e}")

    def get_date_for_moment_and_10_days(self, soup):
        try:
            date = soup.find('main', {'class': ['d66a4e1abc', 'c05bc31d91', 'b19fe90d27']})
            date = date.findAll('div', self.SELECTORS['date_block'])[1]
            return date.text.replace(',', '').split()
        except (AttributeError, IndexError) as e:
            raise WeatherParserError(f"Ошибка извлечения даты: {e}")

    def get_soup_for_moment_and_10_days(self):
        return self.parse_and_soup_page(self.BASE_URL)

    def get_temperature_at_moment(self):
        try:
            soup = self.get_soup_for_moment_and_10_days()
            soup = soup.find('div', self.SELECTORS['current_temp'])
            return self.prettify_temperature(soup)
        except WeatherParserError as e:
            raise WeatherParserError(f"Не удалось получить текущую температуру: {e}")

    def get_temperature_for_10_days(self):
        try:
            soup = self.get_soup_for_moment_and_10_days()
            year = self._extract_year(soup)
            soup = soup.findAll('div', self.SELECTORS['10day_wrapper'])[1]
            slides = soup.findAll('div', self.SELECTORS['day_slide'])
            return [self._create_day_weather(slide, year) for slide in slides]
        except (IndexError, AttributeError) as e:
            raise WeatherParserError(f"Ошибка получения прогноза на 10 дней: {e}")

    def get_temperature_for_month(self, month, year):
        try:
            soup = self.parse_and_soup_page(f"{self.BASE_URL}{month}-{year}/")
            days = soup.findAll('div', self.SELECTORS['calendar_day'])[1:]
            return [self._create_calendar_day(day) for day in days if len(day.text) > 5]
        except Exception as e:
            raise WeatherParserError(f"Ошибка получения месячного прогноза: {e}")

    def _create_day_weather(self, slide, year) -> DayWeather:
        try:
            date = slide.find('div', {'class': ['e6255c6329']}).text + f' {year}'
            temperature = slide.find('div', {'class': ['e487206871', 'a7b7a4c92f']})
            return DayWeather(date, self.prettify_temperature(temperature))
        except Exception as e:
            raise WeatherParserError(f"Ошибка создания DayWeather: {e}")

    def _create_calendar_day(self, day_element) -> DayWeather:
        try:
            date = day_element.find('div', {'class': 'day__date'})
            temperature = day_element.find('div', {'class': 'day__temperature'}).contents[0]
            return DayWeather(
                date=self.prettify_date(date),
                temperature=self.prettify_temperature(temperature)
            )
        except Exception as e:
            raise WeatherParserError(f"Ошибка создания календарного дня: {e}")

    def _extract_year(self, soup) -> str:
        try:
            date_parts = self.get_date_for_moment_and_10_days(soup)
            return date_parts[4] if len(date_parts) > 4 else ""
        except Exception as e:
            raise WeatherParserError(f"Ошибка извлечения года: {e}")