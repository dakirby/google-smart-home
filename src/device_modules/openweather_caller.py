import requests
import datetime


class OpenWeatherCaller():
    def __init__(self, api_key: str, lat: float, lon: float):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon

        self.last_refresh_date = None
        self.latest_response = None
        self._make_call()

    def _make_call(self):
        self.last_refresh_date = datetime.datetime.now().date()
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self.lat}&lon={self.lon}&appid={self.api_key}"

        self.latest_response = requests.get(url).json()

    def update_current_day(self):
        current_date = datetime.datetime.now()

        if self.last_refresh_date < current_date.now().date():
            self._make_call()

    def get_daily_max(self) -> float:
        self.update_current_day()

        max_temp = self.latest_response['daily'][0]['temp']['max'] - 273.15

        return max_temp

    def get_current_temp(self) -> float:
        self._make_call()
        current_temp = self.latest_response['current']['temp'] - 273.15
        return current_temp
