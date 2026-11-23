import random

import pytest

from razbeg import make_data
from razbeg.datasets import KINDS


@pytest.mark.parametrize("kind", KINDS)
def test_size_empty_and_seed(kind):
    assert make_data(kind, 0) == []
    assert len(make_data(kind, 1)) == 1
    assert make_data(kind, 200, 17) == make_data(kind, 200, 17)


@pytest.mark.parametrize("kind", ["random", "nearly", "duplicates"])
def test_different_seeds(kind):
    assert make_data(kind, 500, 17) != make_data(kind, 500, 18)


def test_generator_properties():
    assert make_data("sorted", 5) == [0, 1, 2, 3, 4]
    assert make_data("reverse", 5) == [4, 3, 2, 1, 0]
    nearly = make_data("nearly", 500, 9)
    assert sorted(nearly) == list(range(500))
    assert sum(a != b for a, b in zip(nearly, range(500))) <= 10
    duplicate_data = make_data("duplicates", 200, 9)
    assert len(set(duplicate_data)) <= 16
    assert len(set(duplicate_data)) < len(duplicate_data)


def test_global_random_state_unchanged():
    before = random.getstate()
    make_data("random", 50, 123)
    assert random.getstate() == before


@pytest.mark.parametrize("kind,size,seed,error", [
    ("unknown", 5, 42, ValueError), ("random", -1, 42, ValueError),
    ("random", 2.5, 42, TypeError), ("random", True, 42, TypeError),
    ("random", 5, "42", TypeError),
])
def test_invalid_generator_arguments(kind, size, seed, error):
    with pytest.raises(error):
        make_data(kind, size, seed)
