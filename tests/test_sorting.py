import random

import pytest

from razbeg import insertion_sort, merge_sort


@pytest.mark.parametrize("sorter", [insertion_sort, merge_sort])
@pytest.mark.parametrize("numbers", [
    [], [7], [1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2],
    [-5, 0, -9, 4, -5], [3, 1, 2, 1, 3, 0, -2],
])
def test_basic_cases(sorter, numbers):
    before = numbers.copy()
    answer = sorter(numbers)
    assert answer == sorted(numbers)
    assert numbers == before
    assert answer is not numbers


@pytest.mark.parametrize("sorter", [insertion_sort, merge_sort])
def test_random_cases(sorter):
    rng = random.Random(123)
    for size in range(80):
        numbers = [rng.randint(-100, 100) for _ in range(size)]
        before = numbers.copy()
        assert sorter(numbers) == sorted(numbers)
        assert numbers == before


@pytest.mark.parametrize("sorter", [insertion_sort, merge_sort])
@pytest.mark.parametrize("numbers", [None, (3, 2, 1), "123", [1, "2"], [True], [1.5]])
def test_wrong_types(sorter, numbers):
    with pytest.raises(TypeError):
        sorter(numbers)


def test_merge_large_enough_for_many_blocks():
    rng = random.Random(71)
    numbers = [rng.randint(-500, 500) for _ in range(10003)]
    assert merge_sort(numbers) == sorted(numbers)
