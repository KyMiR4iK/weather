from dayWeather import DayWeather


class WeatherStats:
    def calculate_average_temp(days):
        if not days:
            return 0
        return sum(day.temperature for day in days) / len(days)

    def find_extremes(days):
        if not days:
            return {"max": None, "min": None}
        temps = [day.temperature for day in days]
        return {
            "max": max(temps),
            "min": min(temps),
            "max_day": next(d for d in days if d.temperature == max(temps)),
            "min_day": next(d for d in days if d.temperature == min(temps))
        }

    def get_temp_trend(days):
        if len(days) < 2:
            return "Недостаточно данных"
        
        first = days[0].temperature
        last = days[-1].temperature
        diff = last - first
        
        if diff > 3:
            return "Сильное потепление"
        elif diff > 0:
            return "Слабое потепление"
        elif diff < -3:
            return "Сильное похолодание"
        else:
            return "Слабое похолодание"

    def generate_ascii_chart(days, width=50, height=10):
        temps = [day.temperature for day in days]
        dates = [day.date.split()[0] for day in days]
        
        min_temp = min(temps)
        max_temp = max(temps)
        if min_temp == max_temp:
            return "Недостаточно вариаций температур"
        
        step = (max_temp - min_temp) / height
        chart = []
        
        for level in range(height, -1, -1):
            threshold = min_temp + step * level
            line = "".join("■" if temp >= threshold else " " for temp in temps)
            chart.append(f"{threshold:>4.1f}°C |{line}")
        
        return "\n".join(chart)