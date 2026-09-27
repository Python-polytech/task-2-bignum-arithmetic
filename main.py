DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"

class Number:
    def __init__(self, m: int, n: int, number: str):
        if not 2 <= m <= len(DIGITS):
            raise ValueError("Недопустимое основание системы счисления")
        if n <= 0:
            raise ValueError("Длина числа не может быть меньше одного")
        self.__check_number(number, m)
        self.__check_length(number, n)
        self.m = m
        self.n = n
        self.number = number

    def __add__(self, other):
        if self.m != other.m:
            raise ValueError("Основания системы счисления не совпадают")
        res = self.__transf_to_dec(self.m, self.number) + self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, res)
        result_str = self._normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __sub__(self, other):
        if self.m != other.m:
            raise ValueError("Основания системы счисления не совпадают")
        diff = self.__transf_to_dec(self.m, self.number) - self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, diff)
        result_str = self._normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __mul__(self, other):
        if self.m != other.m:
            raise ValueError("Основания системы счисления не совпадают")
        product = self.__transf_to_dec(self.m, self.number) * self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, product)
        result_str = self._normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __floordiv__(self, other):
        if self.m != other.m:
            raise ValueError("Основания системы счисления не совпадают")
        right = self.__transf_to_dec(other.m, other.number)
        if right == 0:
            raise ZeroDivisionError("Деление на ноль")
        left = self.__transf_to_dec(self.m, self.number)
        result_str = self.__transf_dec_to_m(self.m, left // right)
        result_str = self._normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __str__(self):
        return self.number

    def _normalize(self, result_str: str) -> str:
        sign = "-" if result_str.startswith('-') else ""
        body = result_str[1:] if sign else result_str
        if len(body) > self.n:
            print(f"Переполнение: число обрезано до {self.n} разрядов")
            body = body[-self.n:]
        return sign + body

    @staticmethod
    def __transf_dec_to_m(m: int, number: int) -> str:
        if number == 0:
            return "0"
        sign = "-" if number < 0 else ""
        number = abs(number)
        result = ""
        while number > 0:
            result = DIGITS[number % m] + result
            number //= m
        return sign + result

    @staticmethod
    def __transf_to_dec(m: int, number: str) -> int:
        sign = -1 if number[0] == '-' else 1
        body = number[1:] if sign == -1 else number
        result = 0
        for ch in body:
            result = result * m + int(ch, m)
        return sign * result


    @staticmethod
    def __check_number(number: str, m: int) -> None:
        if not number:
            raise ValueError("Пустая строка не является числом")
        body = number[1:] if number[0] == '-' else number
        if not body:
            raise ValueError("Знак без цифр")
        for s in body:
            try:
                int(s, m)
            except ValueError:
                raise ValueError("Символы в числе превосходят основание системы счисления")

    @staticmethod
    def __check_length(number: str, n: int) -> None:
        body = number[1:] if number and number[0] == '-' else number
        if len(body) > n:
            raise ValueError("Длина числа превосходит заданную")


def print_menu():
    print(f"""
Настройки программы:
    1. Основание системы счисления: {M};
    2. Максимальная разрядность: {N};
Меню действий:
    3. Сложение (+) двух чисел;
    4. Вычитание (-) двух чисел;
    5. Умножение (*) двух чисел;
    6. Целочисленное деление (//) двух чисел;
    7. Выход;
""")

def read_two_numbers():
    raw = input("Введите два числа через пробел: ").strip()
    parts = raw.split()
    if len(parts) != 2:
        raise ValueError("Нужно ровно два числа через пробел")
    return Number(M, N, parts[0]), Number(M, N, parts[1])

def main():
    global M, N

    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        try:
            match choice:
                case "1":
                    new_m = int(input("Новое основание системы счисления: "))
                    if not 2 <= new_m <= 36:
                        raise ValueError("Основание должно быть от 2 до 36")
                    M = new_m

                case "2":
                    new_n = int(input("Новая максимальная разрядность: "))
                    if new_n <= 0:
                        raise ValueError("Разрядность должна быть положительной")
                    N = new_n

                case "3":
                    a, b = read_two_numbers()
                    print("Результат:", a + b)

                case "4":
                    a, b = read_two_numbers()
                    print("Результат:", a - b)

                case "5":
                    a, b = read_two_numbers()
                    print("Результат:", a * b)

                case "6":
                    a, b = read_two_numbers()
                    print("Результат:", a // b)

                case "7":
                    print("Выход.")
                    break

                case _:
                    print("Некорректный пункт, попробуйте снова.")

        except ValueError as e:
            print("Ошибка:", e)
        except ZeroDivisionError as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    M = 10
    N = 5
    main()