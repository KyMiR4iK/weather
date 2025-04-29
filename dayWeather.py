class DayWeather:
    def __init__(self, date, temperature):
        self.date = date
        self.temperature = temperature

    def __str__(self):
        return f"Day(date={self.date}, temperature={self.temperature})"