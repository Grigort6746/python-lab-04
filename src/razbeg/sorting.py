def _check_numbers(numbers: list[int]) -> None:
    if not isinstance(numbers, list):
        raise TypeError("Ожидается список целых чисел")
    if any(type(value) is not int for value in numbers):
        raise TypeError("Каждый элемент должен быть целым числом, без bool")


def insertion_sort(numbers: list[int]) -> list[int]:
    _check_numbers(numbers)
    result = numbers.copy()
    for place in range(1, len(result)):
        current = result[place]
        previous = place - 1
        while previous >= 0 and result[previous] > current:
            result[previous + 1] = result[previous]
            previous -= 1
        result[previous + 1] = current
    return result


def _merge(result: list[int], spare: list[int], left: int, middle: int, right: int) -> None:
    first, second, place = left, middle, left
    while first < middle and second < right:
        if result[first] <= result[second]:
            spare[place] = result[first]
            first += 1
        else:
            spare[place] = result[second]
            second += 1
        place += 1
    if first < middle:
        spare[place:right] = result[first:middle]
    else:
        spare[place:right] = result[second:right]
    result[left:right] = spare[left:right]


def merge_sort(numbers: list[int]) -> list[int]:
    _check_numbers(numbers)
    result = numbers.copy()
    size = len(result)
    spare = [0] * size
    width = 1
    while width < size:
        for left in range(0, size, width * 2):
            middle = min(left + width, size)
            right = min(left + width * 2, size)
            if middle == right or result[middle - 1] <= result[middle]:
                continue
            _merge(result, spare, left, middle, right)
        width *= 2
    return result
