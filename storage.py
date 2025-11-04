import json
import os
import time
from api_client import get_currency_rates

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]

def save_to_file(data: dict, path="currency_rate.json"):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def read_from_file(path="currency_rate.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def is_file_fresh(path, hours=2):
    if not os.path.exists(path):
        return False
    file_age = time.time() - os.path.getmtime(path)
    return file_age < (hours * 3600)

def get_rates(base):
    path = f"rates_{base.lower()}.json"
    
    if is_file_fresh(path):
        try:
            return read_from_file(path)
        except:
            pass
    
    data = get_currency_rates(base)
    if data:
        save_to_file(data, path)
    return data

def update_currency_rates():
    all_data = {}
    for currency in FAVORITE_CURRENCIES:
        rate = get_currency_rates(currency)
        all_data[currency] = rate
    save_to_file(all_data)
    print(f"Данные обновлены в currency_rate.json")