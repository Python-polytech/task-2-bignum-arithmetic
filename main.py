class Number:
    def __init__(self, m: int, n: int, number: int):
        self.__check_number(number, m)
        self.__check_length(number, n)
        self.m = m
        self.n = n
        self.number = number

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __floordiv__(self, other):
        pass

    def __transf_to_dec(self):
        str_number = str(self.number)

    @staticmethod
    def __check_number(number: int, m: int) -> None:
        for s in str(number):
            if s == '-':
                continue
            try:
                int(s, m)
            except ValueError:
                raise ValueError(
                    "Символы в числе превосходят основание системы счисления"
                )

    @staticmethod
    def __check_length(number: int, n: int) -> None:
        if len(str(number)) > n:
            raise ValueError("Длина числа превосходит заданную")



a = Number(4, 5, 1234)

