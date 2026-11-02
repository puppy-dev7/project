from abc import ABC, abstractmethod

# 1. Абстрактный класс для уведомлений
class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass

# Класс для SMS-уведомлений
class SMSNotifier(Notifier):
    def send(self, message):
        print(f"[SMS]: {message}")

# Класс для Telegram-уведомлений
class TelegramNotifier(Notifier):
    def send(self, message):
        print(f"[Telegram]: {message}")


# 2. Основной класс Смартфона
class SmartPhone:
    def __init__(self, name, battery_level, password):
        self.name = name
        self._battery_level = 0      # Задаем начальное значение по умолчанию
        self.battery_level = battery_level  # Здесь срабатывает setter для проверки
        self.__password = password    # Приватный атрибут (инкапсуляция)

    # Геттер для получения уровня заряда
    @property
    def battery_level(self):
        return self._battery_level

    # Сеттер для валидации уровня заряда (не дает установить меньше 0 и больше 100)
    @battery_level.setter
    def battery_level(self, value):
        if 0 <= value <= 100:
            self._battery_level = value
        elif value < 0:
            self._battery_level = 0
        else:
            self._battery_level = 100

    # Метод проверки пароля
    def check_password(self, password):
        return self.__password == password


# 3. ПРОВЕРКА РАБОТЫ ВСЕХ МЕТОДОВ (Вывод в консоль)

print("=== 1. Создание экземпляров с разными значениями ===")
# Создаем 3 телефона с разными параметрами
phone1 = SmartPhone("iPhone 15", 85, "puppy123")
phone2 = SmartPhone("Samsung S24", 140, "secure456")  # Передаем заряд > 100
phone3 = SmartPhone("Xiaomi 14", -25, "admin789")    # Передаем заряд < 0

print(f"Смартфон 1: {phone1.name}, Заряд: {phone1.battery_level}%")
print(f"Смартфон 2 (передали 140%): {phone2.name}, Заряд: {phone2.battery_level}%")
print(f"Смартфон 3 (передали -25%): {phone3.name}, Заряд: {phone3.battery_level}%")


print("\n=== 2. Проверка работы Setter (изменение заряда) ===")
print(f"Текущий заряд {phone1.name}: {phone1.battery_level}%")
phone1.battery_level = 45
print(f"Изменили заряд на 45%: {phone1.battery_level}%")
phone1.battery_level = 200
print(f"Попытались изменить на 200%: {phone1.battery_level}% (сработала защита)")


print("\n=== 3. Проверка работы метода check_password ===")
incorrect_check = phone1.check_password("wrong_pass")
correct_check = phone1.check_password("puppy123")
print(f"Ввели неверный пароль 'wrong_pass': {incorrect_check}")
print(f"Ввели верный пароль 'puppy123': {correct_check}")


print("\n=== 4. Проверка работы классов уведомлений ===")
sms_sender = SMSNotifier()
tg_sender = TelegramNotifier()

sms_sender.send("Внимание! Батарея почти разряжена.")
tg_sender.send("Вам пришло новое сообщение в чате.")
