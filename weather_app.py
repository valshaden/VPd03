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
    while True:
        print("\nРежимы ввода:")
        print("1 — по городу")
        print("2 — по координатам")
        print("0 — выход")
        
        choice = input("Выберите режим: ")
        
        if choice == "0":
            break
        elif choice == "1":
            city = input("Введите название города: ")
            weather = get_current_weather(city=city)
        elif choice == "2":
            latitude = float(input("Введите широту: "))
            longitude = float(input("Введите долготу: "))
            weather = get_current_weather(latitude=latitude, longitude=longitude)
        else:
            print("Неверный выбор!")
            continue
            
        if weather:
            temp = weather['main']['temp']
            description = weather['weather'][0]['description']
            city_name = weather['name']
            print(f"Погода в {city_name}: {temp}°C, {description}")
    