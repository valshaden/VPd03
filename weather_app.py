import os
import json
import logging
import time
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
CACHE_FILE = "weather_cache.json"

logging.basicConfig(filename='weather_errors.log', level=logging.ERROR, 
                   format='%(asctime)s - %(levelname)s - %(message)s')


def make_request_with_retry(url, request_type="запроса"):
    delays = [1, 2, 4]
    
    for attempt in range(4):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            elif response.status_code == 429:
                if attempt < 3:
                    delay = delays[attempt]
                    print(f"Превышен лимит запросов. Повтор через {delay}с...")
                    time.sleep(delay)
                    continue
            return response
        except requests.RequestException as e:
            if attempt < 3:
                delay = delays[attempt]
                print(f"Сетевая ошибка. Повтор {request_type} через {delay}с...")
                time.sleep(delay)
            else:
                raise e
    return None


def save_to_cache(weather_data, city=None, lat=None, lon=None):
    cache_data = {
        "weather": weather_data,
        "city": city,
        "lat": lat,
        "lon": lon,
        "fetched_at": datetime.now().isoformat()
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)


def load_from_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def is_cache_valid(cache_data):
    if not cache_data:
        return False
    fetched_time = datetime.fromisoformat(cache_data["fetched_at"])
    return datetime.now() - fetched_time < timedelta(hours=3)


def offer_cached_data(city=None):
    choice = input("Использовать данные из кэша? (y/n): ")
    if choice.lower() == "y":
        cache = load_from_cache()
        if cache and is_cache_valid(cache):
            if city and cache.get('city', '').lower() == city.lower():
                return cache["weather"]
        print("В кэше информация не найдена")
    return None


def get_current_weather(city: str=None, latitude: float=None, longitude: float=None) -> dict:
    if city:
        print(f"Получаем погоду для города: {city}")
        latitude, longitude = get_coordinates_by_city(city)
        if latitude and longitude:
            return get_weather_by_coordinates(latitude, longitude, city)
        # Если координаты не получены, проверяем кэш
        return offer_cached_data(city)

    if latitude and longitude:
        print(f"Получаем погоду для координат: {latitude}, {longitude}")
        return get_weather_by_coordinates(latitude, longitude)


def get_weather_by_coordinates(latitude: float, longitude: float, city: str = None) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        response = make_request_with_retry(url, "получения погоды")
        if response and response.status_code == 200:
            weather_data = response.json()
            save_to_cache(weather_data, city, latitude, longitude)
            return weather_data
        elif response:
            print(f"Ошибка API: {response.status_code}")
        return offer_cached_data()
    except requests.RequestException as e:
        logging.error(f"Сетевая ошибка при получении погоды: {e}")
        print("Сетевая ошибка при получении погоды")
        return offer_cached_data()

def get_coordinates_by_city(city: str) -> tuple:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}&units=metric&lang=ru"
    
    try:
        response = make_request_with_retry(url, "получения координат")
        if response and response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
        elif response:
            print(f"Ошибка API: {response.status_code}")
        return None, None
    except requests.RequestException as e:
        logging.error(f"Сетевая ошибка при получении координат: {e}")
        print("Сетевая ошибка при получении координат")
        return None, None

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
    