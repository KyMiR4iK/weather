from weatherParser import WeatherParser
from dayWeather import DayWeather
import json


class FileManager:
    def __init__(self, filename: str = "weather_data.json"):
        self.filename = filename
        
    def save_temperature(self, day_weather: 'DayWeather') -> None:
        data = self._load_data()
        
        date_key = day_weather.date
        
        data[date_key] = {
            "date": day_weather.date,
            "temperature": day_weather.temperature
        }
        
        self._save_data(data)
    
    def get_by_date(self, date) -> 'DayWeather':
        data = self._load_data()
        date_key = date
        if date_key in data:
            item = data[date_key]
            return DayWeather(
                date=item["date"],
                temperature=item["temperature"]
            )
        return None
    
    def get_all(self):
        data = self._load_data()
        return [
            DayWeather(
                date=item["date"],
                temperature=item["temperature"]
            )
            for item in data.values()
        ]
    
    def _load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, data) -> None:
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
