import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'users_data.json')

users = {}

def load_data():
    global users
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            print(f"Загружено {len(users)} пользователей")
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            users = {}
            save_data()
    else:
        print("Файл не найден. Создаю новый...")
        users = {}
        save_data()

def save_data():
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
        print("Данные сохранены")
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")

def is_pass_easy(user):
    if user not in users:
        return 'Пользователь не найден!'

    x = users[user]['password']
    
    if len(x) < 8:
        return 'Простой пароль!'
    
    has_letters = False
    has_digits = False
    has_special = False
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    for char in x:
        if char.isalpha():
            has_letters = True
        if char.isdigit():
            has_digits = True
        if char in special_chars:
            has_special = True

    if has_letters and has_digits and has_special:
        return 'Пароль сложный!'
    else:
        return 'Простой пароль!'

def add_user():
    username = input("Введите имя пользователя: ").strip()
    
    if username in users:
        print("Ошибка: пользователь уже существует!")
        return False
    
    email = input("Введите e-mail: ").strip()
    password = input("Введите пароль: ").strip()
    
    city = input("Город: ").strip()
    street = input("Улица: ").strip()
    house = input("Номер дома: ").strip()
    
    other_data = []
    if city:
        other_data.append(city)
    if street:
        other_data.append(street)
    if house:
        other_data.append(house)
    
    users[username] = {
        'e-mail': email,
        'password': password,
        'other': other_data
    }
    
    save_data()
    print('')
    print("Пользователь успешно добавлен!")
    print("Сложность пароля:", is_pass_easy(username))
    
    return True

def debug():
    if not users:
        print("\nСписок пользователей пуст!")
        return
    
    print("\nВсе пользователи:")
    for name in users:
        print("Имя:", name)
        print("Email:", users[name]['e-mail'])
        print("Дополнительные данные:", users[name]['other'])
        print()

def get_data():
    usr = input('Введите имя пользователя: ').strip()
    
    if usr not in users:
        print("Пользователь не найден!")
        return
    
    print(f"\nДанные пользователя '{usr}':")
    print(f"Email: {users[usr]['e-mail']}")
    print(f"Пароль: {users[usr]['password']}")
    print(f"Дополнительные данные: {users[usr]['other']}")

def delete_user():
    username = input("Введите имя пользователя для удаления: ").strip()
    
    if username not in users:
        print("Пользователь не найден!")
        return False
    
    del users[username]
    save_data()
    print(f"Пользователь {username} удален!")
    return True

def main():
    load_data()
    
    while True:
        print("\n=== МЕНЮ ===")
        print("1. Добавить пользователя")
        print("2. Проверить сложность пароля")
        print("3. Показать всех пользователей")
        print("4. Получить данные пользователя")
        print("5. Удалить пользователя")
        print("6. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            add_user()
        elif choice == '2':
            name = input("Введите имя пользователя: ").strip()
            result = is_pass_easy(name)
            print(result)
        elif choice == '3':
            debug()
        elif choice == '4':
            get_data()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            save_data()
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()