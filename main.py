from weatherParser import WeatherParser 
from fileManager import FileManager

weather = WeatherParser()

fileManager = FileManager()

month = weather.get_temperature_for_month('april', 2025)

for i in month:
    fileManager.save_temperature(i)
    print(i)

# print(weather.get_temperature_at_moment())

# print([i.text for i in weather.get_temperature_for_10_days()])

# days = weather.get_temperature_for_10_days()

# for day in days:
#     print(day)

# print('\n\n')
# # Месяц
# month = weather.get_temperature_for_month("may", "2025")
# for day in month:
#     print(day)


