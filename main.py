import re
import requests
from bs4 import BeautifulSoup

PHONE_REGEX = re.compile(
    r'(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}'
)

def validate_phone(phone):
    """Проверяет, соответствует ли номер телефона регулярному выражению."""
    pattern = re.compile(r'^(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}[-\s]?\d{2}[-\s]?\d{2}$')
    return bool(pattern.match(phone))

def search_in_text(text):
    """Ищет все номера телефонов в данном тексте."""
    return PHONE_REGEX.findall(text)

def search_in_url(url):
    """Ищет номера телефонов на веб-странице по URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return search_in_text(text)
    except requests.RequestException as e:
        return []

def search_in_file(file_path):
    """Ищет номера телефонов в локальном файле."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return search_in_text(content)
    except IOError as e:
        return []

def main():
    while True:
        print("\nВыберите опцию:")
        print("1. Ввести номер телефона для проверки")
        print("2. Поиск номеров на веб-странице по URL")
        print("3. Поиск номеров в локальном файле")
        print("4. Выход")
        choice = input("Введите номер опции: ")

        if choice == '1':
            phone = input("Введите номер телефона: ")
            if validate_phone(phone):
                print("Номер телефона корректен.")
            else:
                print("Номер телефона некорректен.")

        elif choice == '2':
            url = input("Введите URL веб-страницы: ")
            phones = search_in_url(url)
            if phones:
                print("Найденные номера телефонов:")
                for p in phones:
                    print(p)
            else:
                print("Номера телефонов не найдены.")

        elif choice == '3':
            file_path = input("Введите путь к файлу: ")
            phones = search_in_file(file_path)
            if phones:
                print("Найденные номера телефонов:")
                for p in phones:
                    print(p)
            else:
                print("Номера телефонов не найдены.")

        elif choice == '4':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
