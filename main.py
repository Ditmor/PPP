from abc import ABC, abstractmethod

# Абстрактный класс для тарифной стратегии
class TariffStrategy(ABC):
    @abstractmethod
    def calculate_cost(self, traffic: float) -> float:
        pass

# Конкретная стратегия тарифа "Стандарт"
class StandardTariff(TariffStrategy):
    def calculate_cost(self, traffic: float) -> float:
        return traffic * 5  # Цена за 1 ГБ

# Конкретная стратегия тарифа "Премиум"
class PremiumTariff(TariffStrategy):
    def calculate_cost(self, traffic: float) -> float:
        return traffic * 3  # Сниженная цена за 1 ГБ

# Класс клиента
class Client:
    def __init__(self, name: str, tariff: TariffStrategy, discount: float = 0.0):
        if discount < 0.01 or discount > 0.5:
            raise ValueError("Скидка должна быть в диапазоне от 1% до 50%")
        self.name = name
        self.tariff = tariff
        self.discount = discount
        self.traffic_used = 0.0

    def add_traffic(self, traffic: float):
        if traffic < 0:
            raise ValueError("Трафик не может быть отрицательным")
        if traffic > 10000:
            raise ValueError("Трафик не может превышать 10000 ГБ")
        self.traffic_used += traffic

    def calculate_cost(self) -> float:
        total_cost = self.tariff.calculate_cost(self.traffic_used)
        return total_cost * (1 - self.discount)

# Класс оператора
class InternetProvider:
    def __init__(self):
        self.clients = []
        self.tariffs = {"standard": StandardTariff, "premium": PremiumTariff}

    def add_tariff(self, name: str, rate: float):
        if rate <= 0 or rate > 10000:
            raise ValueError("Цена за тариф должна быть в диапазоне от 0 до 10000 руб. за ГБ")

        class CustomTariff(TariffStrategy):
            def calculate_cost(self, traffic: float) -> float:
                return traffic * rate

        self.tariffs[name.lower()] = CustomTariff

    def add_client(self, name: str, tariff_name: str, discount: float):
        tariff_class = self.tariffs.get(tariff_name.lower())
        if not tariff_class:
            raise ValueError(f"Неизвестный тариф: {tariff_name}")
        tariff = tariff_class()
        client = Client(name, tariff, discount)
        self.clients.append(client)

    def calculate_total_revenue(self) -> float:
        return sum(client.calculate_cost() for client in self.clients)

    def list_clients(self):
        if not self.clients:
            return "Список клиентов пуст"
        return "\n".join(
            f"{client.name}: {client.traffic_used} ГБ, стоимость: {client.calculate_cost()} руб."
            for client in self.clients
        )

# Интерфейс командной строки
def main():
    provider = InternetProvider()
    print("Добро пожаловать в систему интернет-провайдера.")
    print("Доступные команды:")
    print("1. Добавить клиента")
    print("2. Добавить трафик клиенту")
    print("3. Посчитать общую выручку")
    print("4. Показать список клиентов")
    print("5. Добавить тариф")
    print("6. Выйти из программы")

    while True:
        try:
            command = input("\nВведите номер команды: ").strip()

            if command == "1":
                name = input("Введите имя клиента: ").strip()
                tariff = input("Введите тариф: ").strip()
                discount = float(input("Введите скидку (от 1% до 50%): ").strip()) / 100
                provider.add_client(name, tariff, discount)
                print(f"Клиент {name} добавлен с тарифом {tariff} и скидкой {discount * 100}%.")

            elif command == "2":
                name = input("Введите имя клиента: ").strip()
                traffic = float(input("Введите количество трафика (ГБ): ").strip())
                client = next((c for c in provider.clients if c.name == name), None)
                if client:
                    client.add_traffic(traffic)
                    print(f"{traffic} ГБ добавлено клиенту {name}.")
                else:
                    print(f"Клиент с именем {name} не найден.")

            elif command == "3":
                revenue = provider.calculate_total_revenue()
                print(f"Общая выручка: {revenue} руб.")

            elif command == "4":
                print("Список клиентов:")
                print(provider.list_clients())

            elif command == "5":
                name = input("Введите имя нового тарифа: ").strip()
                rate = float(input("Введите стоимость за 1 ГБ: ").strip())
                provider.add_tariff(name, rate)
                print(f"Тариф {name} добавлен с ценой {rate} руб. за 1 ГБ.")

            elif command == "6":
                print("Выход из программы. До свидания!")
                break

            else:
                print("Неизвестная команда. Попробуйте еще раз.")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
