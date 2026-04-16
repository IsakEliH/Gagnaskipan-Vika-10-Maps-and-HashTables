from collections import namedtuple
from collections.abc import MutableMapping


def polynomial_rolling_hash(s: str) -> int:
    """
    A polynomial rolling hash function using 31 as the multiplier.
    """
    hash_code = 0
    for c in s:
        hash_code = hash_code * 31 + ord(c)
    return hash_code


def h1(s: str) -> int:
    """Hash code generation."""
    return polynomial_rolling_hash(s)


def h2(n: int, max_n: int) -> int:
    """Compresses hash-code into range [0, max_n - 1]."""
    assert max_n > 0, "Invalid max_n"
    return n % max_n


def h(s: str, max_n: int) -> int:
    """Hash function returning a hash value for input string."""
    return h2(h1(s), max_n)


class MyMap(MutableMapping):
    Item = namedtuple("Item", ["key", "value"])

    def __init__(self, size_arr: int = 1, max_load_factor=None):
        assert size_arr > 0, "Invalid array size"
        self._array = [[] for _ in range(size_arr)]
        self._len = 0
        self._max_load_factor = max_load_factor

    def _find(self, key: str) -> tuple[list[Item], int | None]:
        """
        Returns the bucket for key and the index of key in that bucket.
        If key is not present, the index is None.
        """
        bucket = self._array[h(key, len(self._array))]

        for i, item in enumerate(bucket):
            if item.key == key:
                return bucket, i

        return bucket, None

    def _items(self):
        """
        Iterates over all stored Item objects.
        """
        for bucket in self._array:
            for item in bucket:
                yield item

    def _load_factor(self) -> float:
        return self._len / len(self._array)

    def _resize(self) -> None:
        old_items = list(self._items())
        self._array = [[] for _ in range(len(self._array) * 2)]

        for item in old_items:
            bucket = self._array[h(item.key, len(self._array))]
            bucket.append(item)

    def __len__(self) -> int:
        return self._len

    def __iter__(self):
        """
        Iterates over the keys.
        """
        for item in self._items():
            yield item.key

    def __getitem__(self, key):
        bucket, index = self._find(key)

        if index is None:
            raise KeyError(key)

        return bucket[index].value

    def __setitem__(self, key, value) -> None:
        bucket, index = self._find(key)

        if index is not None:
            bucket[index] = self.Item(key, value)
            return

        if (
            self._max_load_factor is not None
            and (self._len + 1) / len(self._array) > self._max_load_factor
        ):
            self._resize()
            bucket, index = self._find(key)

        bucket.append(self.Item(key, value))
        self._len += 1

    def __delitem__(self, key) -> None:
        bucket, index = self._find(key)

        if index is None:
            raise KeyError(key)

        del bucket[index]
        self._len -= 1

    def __str__(self) -> str:
        items = []
        for item in self._items():
            items.append(f"{item.key}: {item.value}")
        return "{" + ", ".join(items) + "}"

    def __repr__(self) -> str:
        return self.__str__()