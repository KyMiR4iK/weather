import os
from datetime import datetime

from weatherParser import WeatherParser
from dayWeather import DayWeather
from weatherStats import WeatherStats
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
    
    def save_multiply_temperatures(self, days):
        for day in days:
            self.save_temperature(day)
    
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
        weather_list = [
            DayWeather(
                date=item["date"],
                temperature=item["temperature"]
            )
            for item in data.values()
        ]
        
        return sorted(weather_list, key=lambda x: self._parse_date(x.date))
    
    def _load_data(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, data) -> None:
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def delete_by_date(self, date: str) -> bool:
        data = self._load_data()
    
        if date in data:
            del data[date]
            self._save_data(data)
            return True
        return False
        
    def clear_all(self) -> None:
        self._save_data({})

    def get_by_date_range(self, start_date: str, end_date: str):
        try:
            start = self._parse_date(start_date)
            end = self._parse_date(end_date)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
        
        data = self._load_data()
        result = []
        
        for date_str, item in data.items():
            try:
                item_date = self._parse_date(item["date"])
                if start <= item_date <= end:
                    result.append(DayWeather(
                        date=item["date"],
                        temperature=item["temperature"]
                    ))
            except ValueError:
                continue
                
        return sorted(result, key=lambda x: self._parse_date(x.date))
    
    def _parse_date(self, date_str: str):
        month_map = {
            'января': 1, 'февраля': 2, 'марта': 3,
            'апреля': 4, 'мая': 5, 'июня': 6,
            'июля': 7, 'августа': 8, 'сентября': 9,
            'октября': 10, 'ноября': 11, 'декабря': 12
        }
        
        try:
            day, month_name, year = date_str.split()
            month = month_map.get(month_name.lower())
            if month is None:
                raise ValueError(f"Unknown month: {month_name}")
            
            return (int(year), month, int(day))
        except Exception as e:
            raise ValueError(f"Failed to parse date '{date_str}': {e}")
        
    def get_stats_for_period(self, start_date: str, end_date: str) -> dict:
        """Получить статистику за период"""
        days = self.get_by_date_range(start_date, end_date)
        return {
            "average": WeatherStats.calculate_average_temp(days),
            "extremes": WeatherStats.find_extremes(days),
            "trend": WeatherStats.get_temp_trend(days),
            "chart": WeatherStats.generate_ascii_chart(days)
        }

    def export_to_txt(self, filename: str = "weather_report.txt") -> str:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        filepath = os.path.join(desktop, filename)
        
        weather_data = self.get_all()
        
        sorted_data = sorted(weather_data, key=lambda x: self._parse_date(x.date))
        
        content = []
        content.append("=" * 50)
        content.append("ПОГОДНЫЙ ОТЧЕТ".center(50))
        content.append(f"Сформирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}".center(50))
        content.append("=" * 50)
        content.append("\n")
        
        months = {}
        for day in sorted_data:
            try:
                day_num, month_name, year = day.date.split()
                month_key = f"{month_name} {year}"
                if month_key not in months:
                    months[month_key] = []
                months[month_key].append(day)
            except:
                continue
        
        for month, days in months.items():
            content.append(f"{month.upper():^50}")
            content.append("-" * 50)
            
            for i in range(0, len(days), 7):
                week = days[i:i+7]
                
                dates_line = " ".join(f"{day.date.split()[0]:>4}" for day in week)
                temps_line = " ".join(f"{day.temperature:>4}°C" for day in week)
                
                content.append(f"Дни:    {dates_line}")
                content.append(f"Температура: {temps_line}")
                content.append("-" * 50)
            
            avg_temp = sum(day.temperature for day in days) / len(days)
            max_day = max(days, key=lambda x: x.temperature)
            min_day = min(days, key=lambda x: x.temperature)
            
            content.append(f"Средняя температура: {avg_temp:.1f}°C")
            content.append(f"Максимальная: {max_day.temperature}°C ({max_day.date.split()[0]} {month})")
            content.append(f"Минимальная:  {min_day.temperature}°C ({min_day.date.split()[0]} {month})")
            content.append("=" * 50)
            content.append("\n")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("\n".join(content))
            return filepath
        except Exception as e:
            raise Exception(f"Ошибка при экспорте в файл: {str(e)}")