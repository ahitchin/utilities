from functools import wraps
from itertools import chain
from sys import getdefaultencoding
from typing import Any, Callable, List, Tuple, Type


class TypeHandler(type):
    __encoding = getdefaultencoding()
    __builtin_binary_sequence_types = (bytes, bytearray, memoryview,)
    __builtin_mapping_types = (dict,)
    __builtin_numeric_types = (int, float, complex,)
    __builtin_sequence_types = (list, tuple, range,)
    __builtin_set_types = (set, frozenset,)
    __builtin_text_sequence_types = (str,)
    __builtin_truth_types = (bool,)

    def merge(func) -> Callable:
        """Merge lists of lists into single tuple."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            def chainer(x: List[Any]) -> List[Any]:
                return tuple(chain(*x))
            result = func(*args, **kwargs)
            return chainer(([result], result)[isinstance(result, (list,))])
        return wrapper

    @property
    @merge
    def binary_types(cls) -> Tuple[Type]:
        """Return all identified relevant standard library binary types."""
        return [
            cls.__builtin_binary_sequence_types,
        ]

    @property
    @merge
    def constant_types(cls) -> Tuple[Type]:
        """Return types which need no conversions within
        recursive transformation functions.
        """
        return [
            cls.__builtin_numeric_types,
            cls.__builtin_text_sequence_types,
            cls.__builtin_truth_types,
        ]

    @property
    @merge
    def iterable_types(cls) -> Tuple[Type]:
        """Return all identified relevant standard library iterable types."""
        return [
            cls.__builtin_sequence_types,
            cls.__builtin_set_types,
        ]

    @property
    @merge
    def mapping_types(cls) -> Tuple[Type]:
        """Return all identified relevant standard library mapping types."""
        return [
            cls.__builtin_mapping_types,
        ]

    @property
    def encoding(cls) -> str:
        """Return systems default encoding."""
        return [
            cls.__encoding,
        ]


class Recurser(metaclass=TypeHandler):
    @classmethod
    def rsnaked(cls, val: Any) -> Any:
        """Recursively change keys to snake case within data structure."""
        if isinstance(val, cls.binary_types):
            return str(val, cls.encoding)
        elif isinstance(val, cls.mapping_types):
            return {cls.snaked(k): cls.rsnaked(v) for k, v in val.items()}
        elif isinstance(val, cls.iterable_types):
            return [cls.rsnaked(x) for x in val]
        elif isinstance(val, cls.constant_types):
            return val

    @classmethod
    def snaked(cls, val: str) -> str:
        """Convert a string to snake case."""
        if len(val) <= 1:
            return val.lower()

        snake = []
        for i in range(len(val) - 1):
            if val[i] != "_" and val[i+1].isupper():
                snake.extend((val[i], "_"))
            elif val[i].isupper():
                snake.append(val[i].lower())
            else:
                snake.append(val[i])
        else:
            snake.append(val[i+1].lower())

        return "".join(snake)
