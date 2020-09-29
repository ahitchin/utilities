#!/usr/bin/env python3.8

from itertools import chain
from queue import Queue
from types import SimpleNamespace
from typing import Any, Generator, List, Tuple


class RecursiveNamespace(SimpleNamespace):
    """Recusively create namespaces for nested structs."""
    def __init__(self, **kwargs: Any) -> None:
        """Recursively create self for nested namespace conversions."""
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            if type(v) == dict:
                setattr(self, k, RecursiveNamespace(**v))
            elif type(v) == list:
                setattr(self, k, list(map(self.__mapper, v)))

    def __mapper(self, val: Any) -> Any:
        """Create self if val is a dictionary, else return the object."""
        if isinstance(val, dict):
            return RecursiveNamespace(**val)
        return val

    def get(self, key: str, default: Any = None) -> Any:
        """dict.get() implementation for namespace."""
        return getattr(self, key, default)

    def items(self) -> List[Tuple[str, Any]]:
        """dict.items() implementation for namespace."""
        items = []
        for key, value in vars(self).items():
            items.append((key, value))
        return items

    def traverse(self) -> Generator:
        """Get all values including nested namespace values."""
        # Stack Setup
        stack = Queue()
        iterator = iter(self)
        current = next(iterator, None)

        # Ensure Namespace isnt Empty
        if current is not None:
            stack.put(current)

        # Until Exausted
        while stack.qsize() != 0:
            # Get and Yield
            current = stack.get()
            yield current

            # Get Next in Generator
            current = next(iterator, None)

            # Chain Generators if Nested Namespace
            if current is not None:
                stack.put(current)
                if isinstance(current[1], self.__class__):
                    iterator = chain(iter(current[1]), iterator)

    def __getitem__(self, key: str) -> Any:
        """Allows obj[var] notation."""
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Allows obj[var] = val notation."""
        setattr(self, key, value)

    def __delitem__(self, key: str) -> None:
        """Allows del obj[key] notation."""
        delattr(self, key)

    def __len__(self) -> int:
        """Get length of attributes in namespace."""
        count = 0
        for _ in self:
            count += 1

        return count

    def __iter__(self) -> Generator:
        """Iterate over attributes."""
        for key, value in vars(self).items():
            yield (key, value)
