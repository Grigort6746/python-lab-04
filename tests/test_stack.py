import pytest

from razbeg import EmptyStackError, Stack


def test_empty():
    pile = Stack[int]()
    assert len(pile) == 0
    assert not pile
    with pytest.raises(EmptyStackError):
        pile.pop()
    with pytest.raises(EmptyStackError):
        pile.peek()


def test_lifo_and_peek():
    pile = Stack[str]()
    pile.push("первая")
    pile.push("вторая")
    assert pile
    assert len(pile) == 2
    assert pile.peek() == "вторая"
    assert pile.peek() == "вторая"
    assert len(pile) == 2
    assert pile.pop() == "вторая"
    assert pile.pop() == "первая"
    assert not pile


def test_size_invariant_after_every_operation():
    pile = Stack[int]()
    for number in range(30):
        pile.push(number)
        assert len(pile) == number + 1
        assert pile.peek() == number
    for number in range(29, -1, -1):
        assert pile.pop() == number
        assert len(pile) == number
        assert bool(pile) == (number > 0)


def test_independent_instances():
    first, second = Stack[int](), Stack[int]()
    first.push(5)
    assert len(second) == 0
