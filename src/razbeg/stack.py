from typing import Generic, TypeVar

T = TypeVar("T")


class EmptyStackError(IndexError):
    pass


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise EmptyStackError("Нельзя извлечь элемент из пустого стека")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise EmptyStackError("Нельзя посмотреть вершину пустого стека")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)
