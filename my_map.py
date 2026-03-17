from collections.abc import MutableMapping
from itertools import chain
from collections import namedtuple


def polynomial_rolling_hash(s):
    """
    A polynomial rolling hash function using a prime number (31) as the multiplier.
    """
    hash_code = 0
    for c in s:
        hash_code = (hash_code * 31) + ord(c)  # ord() returns unicode-value of c
    return hash_code


def h1(s: str) -> int:
    """Hash code generation."""
    # return 0
    # return len(s)
    return polynomial_rolling_hash(s)


def h2(n: int, max_n: int) -> int:
    """Compresses hash-code into range [0, max_n-1]."""
    assert max_n > 0, "Invalid max_n"
    return n % max_n


def h(s: str, max_n: int) -> int:
    """Hash function returning a hash value for input string."""
    return h2(h1(s), max_n)


class MyMap(MutableMapping):
    # Define a named tuple class named 'Item' with fields 'key' and 'value'.
    # This represents a (key, value) pair in our map; create new as: self.Item(key, value)
    Item = namedtuple("Item", ["key", "value"])

    def _in_array(self, bucket: list[Item], key: str) -> int | None:
        """If item with given key is in the array, return its index, otherwise return None."""
        for i in range(len(bucket)):
            if bucket[i].key == key:
                return i
        return None

    def _load_factor(self):
        return self._len / len(self._array)

    def __repr__(self):
        bucket_sizes = []
        for bucket in self._array:
            bucket_sizes.append(len(bucket))
        return str(bucket_sizes)

    def __init__(self, size_arr: int = 1, max_load_factor=None):
        assert size_arr > 0, "Invalid array size"
        self._max_load_factor = max_load_factor  # Do automatically resize when load-factor exceeds max_load_factor
        self._array = [[] for _ in range(size_arr)]
        self._len = 0

    def __iter__(self):
        """
        Returns an iterator; note, for dictionaries one iterates on the keys (not key-value pairs)
        """
        return chain.from_iterable(self._array)  # NOTE: key or not?"

    def __str__(self):
        """
        Returns a string representation of the dictionary (in the same format as Python dict, e.g. {1: 755, 2: 290}
        """
        items = []
        for item in self:
            items.append(f"{item[0]}: {item[1]}")
        return "{" + ", ".join(items) + "}"

    def __len__(self):
        """
        Returns the number of entries in the dictionary.
        """
        return self._len

    # ------------------------------------------------------------------

    def __setitem__(self, key, value):
        """
        Sets (updates if exists, otherwise adds) the value at key entry, i.e. d[key] = value
        """
        if (
            self._max_load_factor is not None
            and 0.0 < self._max_load_factor <= self._load_factor()
        ):
            self._resize()

        bucket_id = h(key, len(self._array))

        key_index = self._in_array(self._array[bucket_id], key)

        x = self.Item(key, value)

        if key_index is not None:
            self._array[bucket_id][key_index] = x

        else:
            self._array[bucket_id].append(x)
            self._len += 1

    def __getitem__(self, key):
        """
        Returns the value at key entry, i.e. value = d[key].
        Raises KeyError if the key is not found.
        """
        bucket_id = h(key, len(self._array))

        key_index = self._in_array(self._array[bucket_id], key)

        if key_index is None:
            raise KeyError(f"Key '{key}' not found in map.")
        
        return self._array[bucket_id][key_index].value


    def __delitem__(self, key):
        """
        Returns the entry at key, i.e. del d[key]
        """
        bucket_id = h(key, len(self._array))

        key_index = self._in_array(self._array[bucket_id], key)

        if key_index is None:
            raise KeyError(f"Key '{key}' not found in map.")
        
        return_value = self._array[bucket_id][key_index].value
        
        del self._array[bucket_id][key_index]

        return return_value
        

    def _resize(self):
        # TO DO ...
        ...


mp = MyMap(2)
print(mp)
print(len(mp))

mp["a"] = 1
print(mp)
print(len(mp))

mp["b"] = 2
print(mp)
print(len(mp))

mp["c"] = 3
print(mp)
print(len(mp))

print(mp["b"])
print(mp)

del mp["a"]
del mp["c"]
del mp["b"]
del mp["b"]
print(mp)
