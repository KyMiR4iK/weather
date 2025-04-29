from weatherParser import WeatherParser 
from fileManager import FileManager

month_dict_eng = {
    1: "january",
    2: "february",
    3: "march",
    4: "april",
    5: "may",
    6: "june",
    7: "july",
    8: "august",
    9: "september",
    10: "october",
    11: "november",
    12: "december"
}
month_dict_rus = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря"
}
choose = -1
print("Это программа для узнавания погоды.")
while choose != 0:
    weather = WeatherParser()
    fileManager = FileManager()
    print("0. Выйти.")
    print("1. Узнать погоду сейчас.")
    print("2. Узнать погоду из интернета на 10 дней.")
    print("3. Узнать погоду из интернета на месяц.")
    print("4. Просмотреть всю запомненную погоду.")
    print("5. Найти сохранённую погоду по дате.")
    print("Введите опцию(число от 1 до 5): ", end = '')
    choose = int(input())
    while not(0<=choose<=5):
        print("Некорректный ввод. Повторите.")
        print("Введите опцию(число от 1 до 5): ", end = '')
        choose = int(input())
    match choose:
        case 0:
            break
        case 1:
            temp = weather.get_temperature_at_moment()
            print(f"Сейчас на улице: {temp} градусов")
        case 2:
            days = weather.get_temperature_for_10_days()
            for day in days:
                print(f"{day.date} температура будет: {day.temperature} градусов")
        case 3:
            print("Введите номер месяца на (от 1 до 12): ", end = '')
            month = int(input())
            while not(1<=month<=12):
                print("Некорректный ввод. Повторите.")
                print("Введите номер месяца на (от 1 до 12): ", end = '')
                month = int(input())
            print("Введите год числом(2009-2026): ", end = '')
            year = int(input())
            while not(2009<=year<=2026):
                print("Некорректный ввод. Повторите.")
                print("Введите год числом(2009-2026): ", end = '')
                year = int(input())
            month = month_dict_eng[month]
            days = weather.get_temperature_for_month(month, year)
            print(days)
            for day in days:
                print(f"{day.date} температура: {day.temperature} градусов")
        case 4:
            days = fileManager.get_all()
            for day in days:
                print(f"{day.date} температура: {day.temperature} градусов")
        case 5:
            print("Введите номер дня на (от 1 до 31): ", end = '')
            day = int(input())
            while not(1<=day<=31):
                print("Некорректный ввод. Повторите.")
                print("Введите номер месяца на (от 1 до 12): ", end = '')
                day = int(input())
            print("Введите номер месяца на (от 1 до 12): ", end = '')
            month = int(input())
            while not(1<=month<=12):
                print("Некорректный ввод. Повторите.")
                print("Введите номер месяца на (от 1 до 12): ", end = '')
                month = int(input())
            print("Введите год числом(2009-2026): ", end = '')
            year = int(input())
            while not(2009<=year<=2026):
                print("Некорректный ввод. Повторите.")
                print("Введите год числом(2009-2026): ", end = '')
                year = int(input())
            month = month_dict_rus[month]
            date = f"{day} {month} {year}"
            day = fileManager.get_by_date(date)
            print(f"{day.date} температура: {day.temperature} градусов")
    choose = -1
print("Пока пока.")