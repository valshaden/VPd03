import requests
import json
import os
import time

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]

def get_currency_rates(base: str) -> dict:
    URL = f"https://open.er-api.com/v6/latest/{base}"

    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: не удалось получить данные для {base}")
        return {}
    
def save_to_file(data: dict, path="currency_rate.json"):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def update_currency_rates():
    all_data = {}
    for currency in FAVORITE_CURRENCIES:
        rate = get_currency_rates(currency)
        all_data[currency] = rate
    save_to_file(all_data)
    print(f"Данные обновлены в currency_rate.json")

def read_from_file(path="currency_rate.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def is_file_fresh(path, hours=24):
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

def show_rates(base, targets=["RUB", "EUR", "GBP"]):
    data = get_rates(base)
    if not data or 'rates' not in data:
        print(f"Не удалось получить курсы для {base}")
        return
    
    print(f"\nКурсы {base}:")
    for currency in targets:
        if currency in data['rates']:
            print(f"1 {base} = {data['rates'][currency]:.4f} {currency}")

def cli():
    while True:
        print("\n1. Обновить курсы валют")
        print("2. Показать курсы валют")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            update_currency_rates()
        elif choice == "2":
            base = input("Введите базовую валюту: ").upper().strip()
            if base:
                show_rates(base)
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    cli()
