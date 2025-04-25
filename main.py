import requests

web_page = "https://pogoda.mail.ru/prognoz/moskva/" # Сайт для парсинга температуры.

request_page = requests.get(web_page)

print(request_page)