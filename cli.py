from storage import get_rates, update_currency_rates

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
        print("3. Обновить курсы")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            base = input("Введите базовую валюту: ").upper().strip()
            if base:
                temp_data = get_rates("USD")
                if temp_data and 'rates' in temp_data:
                    available_currencies = list(temp_data['rates'].keys()) + ["USD"]
                    if not validate_currency(base, available_currencies):
                        continue
                show_rates(base)
        elif choice == "2":
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
        elif choice == "3":
            update_currency_rates()
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    cli()