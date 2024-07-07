from typing import TypeVar

T = TypeVar('T')


def distinct(seq: list[T]) -> list[T]:
    seen: set[T] = set()
    result = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result
