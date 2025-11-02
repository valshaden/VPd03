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

def validate_currency(currency, available_currencies):
    if currency not in available_currencies:
        print(f"Код валюты {currency} не найден")
        return False
    return True

def convert_currency(from_currency, to_currency, amount):
    data = get_rates(from_currency)
    if not data or 'rates' not in data:
        print(f"Не удалось получить курсы для {from_currency}")
        return None
    
    available_currencies = list(data['rates'].keys()) + [from_currency]
    
    if not validate_currency(from_currency, available_currencies):
        return None
    if not validate_currency(to_currency, available_currencies):
        return None
    
    if to_currency not in data['rates']:
        print(f"Валюта {to_currency} не найдена")
        return None
    
    rate = data['rates'][to_currency]
    result = amount * rate
    return result

def cli():
    while True:
        print()
        print("1. Показать курсы валют")
        print("2. Конвертер суммы")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            base = input("Введите базовую валюту: ").upper().strip()
            if base:
                # Получаем список доступных валют для валидации
                temp_data = get_rates("USD")
                if temp_data and 'rates' in temp_data:
                    available_currencies = list(temp_data['rates'].keys()) + ["USD"]
                    if not validate_currency(base, available_currencies):
                        continue
                show_rates(base)
        elif choice == "2":
            # Получаем список доступных валют для валидации
            temp_data = get_rates("USD")
            if temp_data and 'rates' in temp_data:
                available_currencies = list(temp_data['rates'].keys()) + ["USD"]
            else:
                continue
            
            from_currency = input("Из валюты: ").upper().strip()
            if not validate_currency(from_currency, available_currencies):
                continue
            
            to_currency = input("В валюту: ").upper().strip()
            if not validate_currency(to_currency, available_currencies):
                continue
            try:
                amount = float(input("Сумма: "))
                result = convert_currency(from_currency, to_currency, amount)
                if result is not None:
                    print(f"{amount} {from_currency} = {result:.4f} {to_currency}")
            except ValueError:
                print("Неверный формат суммы")
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    cli()
