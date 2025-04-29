from weatherParser import WeatherParser
from fileManager import FileManager

class WeatherApp:
    MONTH_DICT_ENG = {
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
    
    MONTH_DICT_RUS = {
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

    def __init__(self):
        self.weather_parser = WeatherParser()
        self.file_manager = FileManager()
        self.current_choice = -1

    def run(self):
        print("Это программа для узнавания погоды.")
        while self.current_choice != 0:
            self._show_menu()
            self.current_choice = self._get_choice(0, 10)
            self._handle_choice()
        print("Пока пока.")

    def _show_menu(self):
        print("\n0. Выйти.")
        print("1. Узнать погоду сейчас.")
        print("2. Узнать погоду из интернета на 10 дней.")
        print("3. Узнать погоду из интернета на месяц.")
        print("4. Просмотреть всю запомненную погоду.")
        print("5. Найти сохранённую погоду по дате.")
        print("6. Найти промежуток дат.")
        print("7. Статистика за период.")
        print("8. Записать данные в текстовый документ на рабочем столе.")
        print("9. Удалить запись даты.")
        print("10. Удалить все данные.")

    def _get_choice(self, min_val: int, max_val: int) -> int:
        while True:
            try:
                choice = int(input(f"Введите опцию (число от {min_val} до {max_val}): "))
                if min_val <= choice <= max_val:
                    return choice
                print(f"Ошибка: введите число от {min_val} до {max_val}")
            except ValueError:
                print("Ошибка: введите целое число")

    def _get_date_input(self):
        day = self._get_choice(1, 31)
        month = self._get_choice(1, 12)
        year = self._get_choice(2009, 2026)
        return day, month, year

    def _print_weather_data(self, days, header: str = ""):
        if not days:
            print("\nНет данных для отображения.\n")
            return
        
        print("\n" + "-" * 40)
        if header:
            print(header.center(40))
            print("-" * 40)
        print(f"{'Дата':<20}{'Температура':>10}")
        print("-" * 40)
        for day in days:
            print(f"{day.date:<20}{day.temperature:>10}°C")
        print("-" * 40 + "\n")

    def _handle_choice(self):
        match self.current_choice:
            case 1:
                self._handle_current_weather()
            case 2:
                self._handle_10_days_forecast()
            case 3:
                self._handle_month_forecast()
            case 4:
                self._handle_all_saved_weather()
            case 5:
                self._handle_search_by_date()
            case 6:
                self._handle_search_by_range()
            case 7:
                self._handle_stats()
            case 8:
                self._handle_export()
            case 9:
                self._handle_delete_by_date()
            case 10:
                self._handle_delete_all()

    def _handle_current_weather(self):
        temp = self.weather_parser.get_temperature_at_moment()
        print(f"\nСейчас на улице: {temp}°C\n")

    def _handle_10_days_forecast(self):
        days = self.weather_parser.get_temperature_for_10_days()
        self._print_weather_data(days, "Прогноз на ")
        self.file_manager.save_multiply_temperatures(days)

    def _handle_month_forecast(self):
        print("\nЗапрос погоды на месяц:")
        month_num = self._get_choice(1, 12)
        year = self._get_choice(2009, 2026)
        month_name_eng = self.MONTH_DICT_ENG[month_num]
        month_name_rus = self.MONTH_DICT_RUS[month_num]
        
        days = self.weather_parser.get_temperature_for_month(month_name_eng, year)
        
        if not days:
            print(f"\nНе удалось получить данные за {month_name_rus} {year} года.\n")
            return
        
        header = f"Прогноз погоды на {month_name_rus} {year} года"
        self._print_weather_data(days, header)

        self.file_manager.save_multiply_temperatures(days)

    def _handle_all_saved_weather(self):
        days = self.file_manager.get_all()
        if not days:
            print("\nНет сохранённых данных о погоде.\n")
            return
        self._print_weather_data(days, "Сохранено: ")

    def _handle_search_by_date(self):
        print("\nПоиск погоды по дате:")
        day, month_num, year = self._get_date_input()
        month_name = self.MONTH_DICT_RUS[month_num]
        date_str = f"{day} {month_name} {year}"
        
        weather_data = self.file_manager.get_by_date(date_str)
        if weather_data:
            self._print_weather_data([weather_data], "Найдено: ")
        else:
            print(f"\nДанные за {date_str} не найдены.\n")

    def _handle_search_by_range(self):
        day1, month_num1, year1 = self._get_date_input()
        month_name1 = self.MONTH_DICT_RUS[month_num1]
        date_str1 = f"{day1} {month_name1} {year1}"

        day2, month_num2, year2 = self._get_date_input()
        month_name2 = self.MONTH_DICT_RUS[month_num2]
        date_str2 = f"{day2} {month_name2} {year2}"

        days = self.file_manager.get_by_date_range(date_str1, date_str2)

        if not days:
            print(f"\nНе удалось получить данные c {date_str1} {month_name1} {year1} по {date_str2} {month_name2} {year2}.\n")
            return
        
        header = f"Прогноз погоды c {date_str1} {month_name1} {year1} по {date_str2} {month_name2} {year2}:\n"
        self._print_weather_data(days, header)
    
    def _handle_stats(self):
        print("\nСтатистика за период:")
        print("Введите начальную дату:")
        start = self._get_date_input()
        print("Введите конечную дату:")
        end = self._get_date_input()
        
        start_str = f"{start[0]} {self.MONTH_DICT_RUS[start[1]]} {start[2]}"
        end_str = f"{end[0]} {self.MONTH_DICT_RUS[end[1]]} {end[2]}"
        
        stats = self.file_manager.get_stats_for_period(start_str, end_str)
        
        print(f"\nСредняя температура: {stats['average']:.1f}°C")
        print(f"Максимум: {stats['extremes']['max']}°C ({stats['extremes']['max_day'].date})")
        print(f"Минимум: {stats['extremes']['min']}°C ({stats['extremes']['min_day'].date})")
        print(f"Тренд: {stats['trend']}")
        print("\nГрафик температур:")
        print(stats['chart'])

    def _handle_export(self):
        try:
            filepath = self.file_manager.export_to_txt()
            print(f"\nДанные успешно экспортированы в файл: {filepath}")
            print("Файл сохранен на рабочем столе.")
        except Exception as e:
            print(f"\nОшибка при экспорте данных: {e}")

    def _handle_delete_by_date(self):
        day, month_num, year = self._get_date_input()
        month_name = self.MONTH_DICT_RUS[month_num]
        date_str = f"{day} {month_name} {year}"
        self.file_manager.delete_by_date(date_str)
        print("Запись удалена!")

    def _handle_delete_all(self):
        self.file_manager.clear_all()
        print("Все данные удалены!")

def main():
    app = WeatherApp()
    app.run()


if __name__ == "__main__":
    main()