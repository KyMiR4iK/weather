from weatherParser import WeatherParser 

weather = WeatherParser()

# print(weather.get_temperature_at_moment())

# print([i.text for i in weather.get_temperature_for_10_days()])

days = weather.get_temperature_for_10_days()

for day in days:
    print(day)


# Месяц
# month = weather.get_temperature_for_month("may", "2025")
# for day in month:
#     print(day)