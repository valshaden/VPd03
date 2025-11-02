import requests
import json

FAVORITE_CURRENCIES = ["USD", "EUR", "GBP", "RUB"]

def get_currency_rate(currency_code: str):
    URL = f"https://open.er-api.com/v6/latest/{currency_code}"

    try:
        response = requests.get(URL, timeout=10)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    if response.status_code != 200: 
        print(f"Ошибка: {response.status_code}")
        return None
    
    try:
        data = response.json()
        return data
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON")
        return None
    
def save_to_file(data: dict):
    try:
        with open("currency_rate.json", "w") as file:
            json.dump(data, file)
    except (OSError, PermissionError, json.JSONEncodeError) as e:
        print(f"Ошибка сохранения: {e}")

def update_currency_rates():
    all_data = {}
    for currency in FAVORITE_CURRENCIES:
        rate = get_currency_rate(currency)
        if rate is not None:
            all_data[currency] = rate

    save_to_file(all_data)
    print(f"Данные обновлены в currency_rate.json")

def read_from_file():
    try:
        with open("currency_rate.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print(f"Ошибка чтения: {e}")
        return None

def get_available_currencies():
    data = read_from_file()
    if not data:
        return []
    
    currencies = set()
    for base_currency, rates_data in data.items():
        currencies.add(base_currency)
        if 'rates' in rates_data:
            currencies.update(rates_data['rates'].keys())
    return sorted(list(currencies))

def convert_currency(from_currency, to_currency, amount=1):
    data = read_from_file()
    if not data:
        return None
    
    # Прямое конвертирование
    if from_currency in data and 'rates' in data[from_currency]:
        if to_currency in data[from_currency]['rates']:
            rate = data[from_currency]['rates'][to_currency]
            return amount * rate
    
    # Обратное конвертирование
    if to_currency in data and 'rates' in data[to_currency]:
        if from_currency in data[to_currency]['rates']:
            rate = data[to_currency]['rates'][from_currency]
            return amount / rate
    
    return None

def currency_interface():
    print("Конвертер валют")
    print("=" * 20)
    
    currencies = get_available_currencies()
    if not currencies:
        print("Нет доступных валют. Обновите данные.")
        return
    
    print(f"Доступные валюты: {', '.join(currencies)}")
    
    while True:
        try:
            from_currency = input("Введите валюту из (Enter для выхода): ").upper().strip()
            if not from_currency:
                break
            
            to_currency = input("Введите валюту в: ").upper().strip()
            amount = float(input("Введите сумму (1): ") or "1")
            
            result = convert_currency(from_currency, to_currency, amount)
            if result is not None:
                print(f"{amount} {from_currency} = {result:.4f} {to_currency}")
            else:
                print("Не удалось конвертировать валюты")
            print()
            
        except ValueError:
            print("Некорректная сумма")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    while True:
        print("\n0. Выход")
        print("1. Обновить курсы валют")
        print("2. Конвертер валют")
        choice = input("Выберите действие (0-2): ").strip()
        
        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            update_currency_rates()
        elif choice == "2":
            currency_interface()
        else:
            print("Некорректный выбор. Попробуйте снова.")
