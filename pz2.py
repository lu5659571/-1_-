import math

class Circle:
    def __init__(self, radius=1.0):
        self.radius = radius

    @property
    def radius(self):
        return self.__radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Радиус должен быть положительным числом!")
        self.__radius = value

    def read(self):
        while True:
            try:
                val = float(input("Введите радиус круга: "))
                self.radius = val
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Попробуйте еще раз.")

    def display(self):
        print("-" * 30)
        print(f"Текущий радиус: {self.radius}")
        print(f"Площадь круга: {self.area():.2f}")
        print(f"Длина окружности: {self.circumference():.2f}")
        print("-" * 30)

    def area(self):
        """Вычисление площади круга (π × r²)"""
        return math.pi * (self.radius ** 2)

    def circumference(self):
        """Вычисление длины окружности (2 × π × r)"""
        return 2 * math.pi * self.radius

if __name__ == '__main__':
    my_circle = Circle()

    my_circle.read()

    my_circle.display()