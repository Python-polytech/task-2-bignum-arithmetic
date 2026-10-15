class NumberError(Exception):
    """Базовое исключение для всех ошибок класса Number."""


class InvalidBaseError(NumberError, ValueError):
    """Основание системы счисления вне допустимого диапазона."""


class InvalidLengthError(NumberError, ValueError):
    """Некорректная максимальная разрядность."""


class InvalidNumberError(NumberError, ValueError):
    """Некорректная запись числа."""


class BaseMismatchError(NumberError, ValueError):
    """Основания систем счисления операндов не совпадают."""


class DivisionByZeroError(NumberError, ZeroDivisionError):
    """Деление на ноль."""

class Number:
    def __init__(self, m: int, n: int, number: str):
        if not 2 <= m <= 10**6:
            raise InvalidBaseError("Недопустимое основание системы счисления")
        if n <= 0:
            raise InvalidLengthError("Длина числа не может быть меньше одного")
        self.__check_number(number, m)
        self.__check_length(number, n)
        self.m = m
        self.n = n
        self.number = number

    def __add__(self, other):
        if self.m != other.m:
            raise BaseMismatchError("Основания системы счисления не совпадают")
        res = self.__transf_to_dec(self.m, self.number) + self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, res)
        result_str = self.__normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __sub__(self, other):
        if self.m != other.m:
            raise BaseMismatchError("Основания системы счисления не совпадают")
        diff = self.__transf_to_dec(self.m, self.number) - self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, diff)
        result_str = self.__normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __mul__(self, other):
        if self.m != other.m:
            raise BaseMismatchError("Основания системы счисления не совпадают")
        product = self.__transf_to_dec(self.m, self.number) * self.__transf_to_dec(other.m, other.number)
        result_str = self.__transf_dec_to_m(self.m, product)
        result_str = self.__normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __floordiv__(self, other):
        if self.m != other.m:
            raise BaseMismatchError("Основания системы счисления не совпадают")
        right = self.__transf_to_dec(other.m, other.number)
        if right == 0:
            raise DivisionByZeroError("Деление на ноль")
        left = self.__transf_to_dec(self.m, self.number)
        result_str = self.__transf_dec_to_m(self.m, left // right)
        result_str = self.__normalize(result_str)
        return Number(self.m, self.n, result_str)

    def __str__(self):
        return self.number

    def __normalize(self, result_str: str) -> str:
        """Нормализация длины числа до длины self.n. Если число больше, старшие разряды отбрасываются."""
        sign = "-" if result_str.startswith('-') else ""
        body = result_str[1:] if sign else result_str
        digits = body.split('#')
        if len(digits) > self.n:
            print(f"Переполнение: число обрезано до {self.n} разрядов")
            digits = digits[-self.n:]
        return sign + "#".join(digits)

    @staticmethod
    def __transf_dec_to_m(m: int, number: int) -> str:
        """Перевод из десятичной системы счисления в m-ричную."""
        if number == 0:
            return "0"
        sign = "-" if number < 0 else ""
        number = abs(number)
        result = []
        while number > 0:
            result.append(str(number % m))
            number //= m
        result.reverse()
        return sign + "#".join(result)

    @staticmethod
    def __transf_to_dec(m: int, number: str) -> int:
        """Перевод из m-ричной системы счисления в десятичную."""
        sign = -1 if number[0] == '-' else 1
        body = number[1:] if sign == -1 else number
        result = 0
        for part in body.split('#'):
            digit = int(part)
            result = result * m + digit
        return sign * result


    @staticmethod
    def __check_number(number: str, m: int) -> None:
        """Валидация ввода числа."""
        if not number:
            raise InvalidNumberError("Пустая строка не является числом")
        body = number[1:] if number[0] == '-' else number
        if not body:
            raise InvalidNumberError("Знак без цифр")
        for part in body.split('#'):
            if part == "":
                raise InvalidNumberError("Пустой разряд между разделителем")
            try:
                digit = int(part)
            except ValueError:
                raise InvalidNumberError(f"Разряд '{part}' не является целым числом") from None
            if not 0 <= digit < m:
                raise InvalidNumberError(f"Разряд {digit} превосходит основание системы счисления")

    @staticmethod
    def __check_length(number: str, n: int) -> None:
        body = number[1:] if number and number[0] == '-' else number
        digits = body.split('#')
        if len(digits) > n:
            raise InvalidLengthError("Длина числа превосходит заданную")


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
    raw = input("Введите два числа через пробел, разряды через '#' (пример: 1#5 3#0): ").strip()
    parts = raw.split()
    if len(parts) != 2:
        raise InvalidNumberError("Нужно ровно два числа через пробел")
    return Number(M, N, parts[0]), Number(M, N, parts[1])

def main():
    global M, N

    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        try:
            match choice:
                case "1":
                    try:
                        new_m = int(input("Новое основание системы счисления: "))
                    except ValueError:
                        raise InvalidBaseError("Основание должно быть целым числом")
                    if not 2 <= new_m <= 10 ** 6:
                        raise InvalidBaseError("Основание должно быть от 2 до 1000000")
                    M = new_m

                case "2":
                    try:
                        new_n = int(input("Новая максимальная разрядность: "))
                    except ValueError:
                        raise InvalidLengthError("Разрядность должна быть целым числом")
                    if new_n <= 0:
                        raise InvalidLengthError("Разрядность должна быть положительной")
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

        except NumberError as e:
            print("Ошибка:", e)


if __name__ == "__main__":
    M = 23
    N = 10
    main()