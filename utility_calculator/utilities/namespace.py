from types import SimpleNamespace
from typing import Any, Generator


class RecursiveNamespace(SimpleNamespace):
    """Recusively create Namespaces for nested structs."""

    def __init__(self, **kwargs: Any) -> None:
        """Recursively create self for nested namespace conversions."""
        super().__init__(**kwargs)
        for k, v in kwargs.items():
            if type(v) == dict:
                setattr(self, k, RecursiveNamespace(**v))
            elif type(v) == list:
                setattr(self, k, list(map(self.mapper, v)))

    @staticmethod
    def mapper(val: Any) -> Any:
        """Create self if val is a dictionary, else return the object."""
        if isinstance(val, dict):
            return RecursiveNamespace(**val)
        return val

    def __iter__(self) -> Generator:
        """Dynamically iter over attributes."""
        for key, value in vars(self).items():
            yield (key, value)
