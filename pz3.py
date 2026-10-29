# ==========================================
# 1. КАСТОМНЫЕ ИСКЛЮЧЕНИЯ (Шаг 2.3)
# ==========================================
class InvalidPriceError(ValueError):
    """Исключение: некорректная цена."""
    pass


class InvalidMonthsError(ValueError):
    """Исключение: некорректное количество месяцев."""
    pass


class AssetLimitExceededError(Exception):
    """Исключение: превышен лимит стоимости техники на сотрудника."""
    pass


# ==========================================
# 2. БАЗОВЫЙ КЛАСС И ПОЛИМОРФИЗМ (Шаг 2.1)
# ==========================================
class ITAsset:
    def __init__(self, inventory_id, name, initial_price, months_used=0):
        self.inventory_id = inventory_id
        self.name = name

        # Используем сеттеры для валидации при создании
        self.initial_price = initial_price
        self.months_used = months_used

    # --- Сеттеры с проверками (Шаг 2.3) ---
    @property
    def initial_price(self):
        return self._initial_price

    @initial_price.setter
    def initial_price(self, value):
        if value <= 0:
            raise InvalidPriceError(f"Цена должна быть больше 0, получено: {value}")
        self._initial_price = value

    @property
    def months_used(self):
        return self._months_used

    @months_used.setter
    def months_used(self, value):
        if value < 0:
            raise InvalidMonthsError(f"Количество месяцев не может быть отрицательным, получено: {value}")
        self._months_used = value

    # --- Полиморфный метод (переопределяется в наследниках) ---
    def calculate_residual_value(self):
        """Базовая реализация (будет переопределена)."""
        return 0

    # --- МАГИЧЕСКИЕ МЕТОДЫ (Шаг 2.2) ---

    # 1. __str__ - для пользователя
    def __str__(self):
        return (f"[{self.inventory_id}] {self.name} | "
                f"Остаток: {self.calculate_residual_value():.2f} руб. "
                f"(Износ: {self.months_used} мес.)")

    # 2. __repr__ - для разработчика
    def __repr__(self):
        return f"{self.__class__.__name__}(id='{self.inventory_id}', price={self.initial_price}, months={self.months_used})"

    # 3. __eq__ - сравнение по инвентарному номеру
    def __eq__(self, other):
        if not isinstance(other, ITAsset):
            return NotImplemented
        return self.inventory_id == other.inventory_id

    # 4. __lt__ - сравнение по остаточной стоимости (для сортировки)
    def __lt__(self, other):
        return self.calculate_residual_value() < other.calculate_residual_value()

    # 5. __add__ - сложение остаточных стоимостей
    def __add__(self, other):
        if isinstance(other, ITAsset):
            return self.calculate_residual_value() + other.calculate_residual_value()
        return NotImplemented

    # 6. __sub__ - списание (увеличение износа)
    def __sub__(self, months_to_write_off):
        if not isinstance(months_to_write_off, int):
            raise TypeError("Списывать можно только целое число месяцев")

        new_months = self.months_used + months_to_write_off
        if new_months > self.lifetime_months:
            new_months = self.lifetime_months  # Не уходим в минус по сроку

        # Создаем НОВЫЙ объект с обновленными данными (по заданию)
        return self.__class__(self.inventory_id, self.name, self.initial_price, new_months)


# ==========================================
# 3. КЛАССЫ-НАСЛЕДНИКИ (Полиморфизм)
# ==========================================
class Laptop(ITAsset):
    lifetime_months = 36

    def calculate_residual_value(self):
        # Формула: price * max(0, 1 - months / lifetime)
        return self.initial_price * max(0, 1 - self.months_used / self.lifetime_months)


class Monitor(ITAsset):
    lifetime_months = 60

    def calculate_residual_value(self):
        return self.initial_price * max(0, 1 - self.months_used / self.lifetime_months)


class Smartphone(ITAsset):
    lifetime_months = 24

    def calculate_residual_value(self):
        return self.initial_price * max(0, 1 - self.months_used / self.lifetime_months)


# ==========================================
# 4. КЛАСС-КОНТЕЙНЕР (Шаг 2.4)
# ==========================================
class EmployeeAssets:
    def __init__(self, employee_name, limit=150000):
        self.employee_name = employee_name
        self.limit = limit
        self._assets = []

    def add_asset(self, asset):
        """Добавление техники с проверкой лимита."""
        current_total = sum(a.calculate_residual_value() for a in self._assets)
        new_total = current_total + asset.calculate_residual_value()

        if new_total > self.limit:
            raise AssetLimitExceededError(
                f"Нельзя выдать {asset.name}! Превышен лимит на {new_total - self.limit:.2f} руб. "
                f"(Текущая сумма: {current_total:.2f}, Лимит: {self.limit})"
            )
        self._assets.append(asset)

    # Магический метод для len()
    def __len__(self):
        return len(self._assets)

    # Магический метод для доступа по индексу []
    def __getitem__(self, index):
        return self._assets[index]


# ==========================================
# 5. ДЕМОНСТРАЦИЯ РАБОТЫ (ЭТАП 3)
# ==========================================
if __name__ == "__main__":
    print("=== 1. СОЗДАНИЕ ОБЪЕКТОВ ===")
    # Создаем технику
    laptop = Laptop(inventory_id="INV-001", name="Ноутбук Dell", initial_price=80000, months_used=18)
    monitor = Monitor(inventory_id="INV-002", name="Монитор LG", initial_price=25000, months_used=12)
    phone = Smartphone(inventory_id="INV-003", name="Смартфон iPhone", initial_price=40000, months_used=6)

    print("Демонстрация __str__:")
    print(laptop)
    print(monitor)
    print(phone)

    print("\n=== 2. МАГИЧЕСКИЕ МЕТОДЫ ===")
    print(f"Сложение (__add__): {laptop.name} + {monitor.name} = {laptop + monitor} руб.")

    # Демонстрация __sub__ (списание 6 месяцев)
    laptop_written_off = laptop - 6
    print(f"Списание (__sub__): {laptop.name} после 6 мес. -> {laptop_written_off}")

    # Проверка равенства (__eq__)
    laptop_copy = Laptop(inventory_id="INV-001", name="Ноутбук Dell (копия)", initial_price=80000)
    print(f"Сравнение (__eq__) по ID: {laptop == laptop_copy}")

    print("\n=== 3. КОНТЕЙНЕР И СОРТИРОВКА ===")
    employee_bag = EmployeeAssets("Иванов Иван")
    employee_bag.add_asset(laptop)
    employee_bag.add_asset(monitor)
    employee_bag.add_asset(phone)

    print(f"Техники в контейнере (len): {len(employee_bag)}")
    print(f"Первый элемент по индексу [0]: {employee_bag[0].name}")

    # Сортировка (использует __lt__ по остаточной стоимости)
    print("\nСортировка по остаточной стоимости (от дешевой к дорогой):")
    sorted_assets = sorted(employee_bag._assets)
    for asset in sorted_assets:
        print(asset)

    print("\n=== 4. ОБРАБОТКА ИСКЛЮЧЕНИЙ ===")

    # 1. Попытка добавить технику сверх лимита
    try:
        # Сейчас сумма ~ 90000. Добавим еще один ноутбук за 80 000 (превысит 150 000)
        new_laptop = Laptop(inventory_id="INV-004", name="Игровой ПК", initial_price=80000)
        employee_bag.add_asset(new_laptop)
    except AssetLimitExceededError as e:
        print(f"[Перехвачено исключение]: {e}")

    # 2. Попытка создать технику с отрицательной ценой
    try:
        bad_asset = Monitor(inventory_id="INV-005", name="Сломанный монитор", initial_price=-5000)
    except InvalidPriceError as e:
        print(f"[Перехвачено исключение]: {e}")