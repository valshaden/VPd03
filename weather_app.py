import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_current_weather(city: str=None, latitude: float=None, longitude: float=None) -> dict:

    if city:
        print(f"Получаем погоду для города: {city}")
        latitude, longitude = get_coordinates_by_city(city)
        weather = get_weather_by_coordinates(latitude, longitude)
        return weather

    if latitude and longitude:
        print(f"Получаем погоду для координат: {latitude}, {longitude}")
        return get_weather_by_coordinates(latitude, longitude)


def get_weather_by_coordinates(latitude: float, longitude: float) -> dict:

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=ru"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        return None

def get_coordinates_by_city(city: str) -> dict:

    #http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()[0]['lat'], response.json()[0]['lon']
    else:
        print(f"Ошибка: {response.status_code}")
        return None

if __name__ == "__main__":

    print(API_KEY)
    weather = get_current_weather(city="Приморск")
    print(weather)
    #weather = get_weather_by_coordinates(55.7558, 37.6173)
    #print(weather)
    