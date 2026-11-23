import random

KINDS = ("random", "sorted", "reverse", "nearly", "duplicates")


def make_data(kind: str, size: int, seed: int = 42) -> list[int]:
    if type(size) is not int:
        raise TypeError("Размер должен быть целым числом")
    if size < 0:
        raise ValueError("Размер не может быть отрицательным")
    if type(seed) is not int:
        raise TypeError("Seed должен быть целым числом")
    if kind not in KINDS:
        raise ValueError(f"Неизвестный набор: {kind}")

    rng = random.Random(seed)
    if kind == "random":
        return [rng.randint(-size, size) for _ in range(size)]
    if kind == "sorted":
        return list(range(size))
    if kind == "reverse":
        return list(range(size - 1, -1, -1))
    if kind == "duplicates":
        return [rng.randint(-8, 7) for _ in range(size)]

    result = list(range(size))
    if size > 1:
        for _ in range(max(1, size // 100)):
            place = rng.randrange(size - 1)
            result[place], result[place + 1] = result[place + 1], result[place]
    return result
