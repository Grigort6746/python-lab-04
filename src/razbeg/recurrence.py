def _check_pair(a: int, b: int) -> None:
    if type(a) is not int or type(b) is not int:
        raise TypeError("Аргументы НОД должны быть целыми числами")
    if a < 0 or b < 0 or (a == 0 and b == 0):
        raise ValueError("Нужны неотрицательные числа, хотя бы одно больше нуля")


def gcd_loop(a: int, b: int) -> int:
    _check_pair(a, b)
    while b != 0:
        a, b = b, a % b
    return a


def _gcd_step(a: int, b: int) -> int:
    if b == 0:
        return a
    return _gcd_step(b, a % b)


def gcd_recursive(a: int, b: int) -> int:
    _check_pair(a, b)
    return _gcd_step(a, b)
