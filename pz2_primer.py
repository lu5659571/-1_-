class AverageCalculator:
    def get_average(self, *args):
        if not args:
            return 0
        return sum(args) / len(args)


if __name__ == "__main__":
    numbers = []
    print("Введите числа для расчета среднего значения.")
    print("Для завершения нажмите Enter (пустая строка).")

    while True:
        user_input = input("Введите число: ")
        if user_input == "":
            break
        try:
            numbers.append(float(user_input))
        except ValueError:
            print("Ошибка: введите корректное числовое значение.")

    calc = AverageCalculator()
    avg = calc.get_average(*numbers)
    print(f"Среднее значение введенных чисел: {avg:.2f}")