from functools import partial, wraps
from itertools import chain
from sys import getdefaultencoding
from types import SimpleNamespace
from typing import Any, Dict, Tuple, Type, Union

class TypeHandler(type):
    __encoding = getdefaultencoding()
    __builtin_binary_sequence_types = (bytes, bytearray, memoryview,)
    __builtin_mapping_types = (dict,)
    __builtin_numeric_types = (int, float, complex,)
    __builtin_sequence_types = (list, tuple, range,)
    __builtin_set_types = (set, frozenset,)
    __builtin_text_sequence_types = (str,)
    __builtin_truth_types = (bool,)
   
    def merge(func):
        """Merge lists of lists into single tuple"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            call = lambda x: tuple(chain(*x))
            result = func(*args, **kwargs)
            return call(([result], result)[isinstance(result, (list,))])
        return wrapper

    @property
    @merge
    def binary_types(self) -> Tuple[Type]:
        """Return all identified relevant standard library binary types"""
        return self.builtin_binary_sequence_types

    @property
    @merge
    def constant_types(self) -> Tuple[Type]:
        """Return types which need no conversions within recursive transformation functions"""
        return [
            self.builtin_numeric_types,
            self.builtin_text_sequence_types,
            self.builtin_truth_types,
        ]
    
    @property
    @merge
    def iterable_types(self) -> Tuple[Type]:
        """Return all identified relevant standard library iterable types"""
        return [
            self.builtin_sequence_types,
            self.builtin_set_types,
        ]
    
    @property
    @merge
    def mapping_types(self) -> Tuple[Type]:
        """Return all identified relevant standard library mapping types"""
        return [
            self.builtin_mapping_types,
        ]

    @property
    def encoding(cls) -> str:
        """Return systems default encoding."""
        return cls.__encoding
    
    @property
    def builtin_binary_sequence_types(cls) -> Tuple[Type]:
        """Return python builtin binary sequence types."""
        return cls.__builtin_binary_sequence_types

    @property
    def builtin_sequence_types(cls) -> Tuple[Type]:
        """Return python builtin sequence types."""
        return cls.__builtin_sequence_types

    @property
    def builtin_mapping_types(cls) -> Tuple[Type]:
        """Return python builtin mapping types."""
        return cls.__builtin_mapping_types

    @property
    def builtin_numeric_types(cls) -> Tuple[Type]:
        """Return python builtin numeric types."""
        return cls.__builtin_numeric_types
    
    @property
    def builtin_set_types(cls) -> Tuple[Type]:
        """Return python builtin set sequence types."""
        return cls.__builtin_set_types

    @property
    def builtin_text_sequence_types(cls) -> Tuple[Type]:
        """Return python builtin text sequence types."""
        return cls.__builtin_text_sequence_types

    @property
    def builtin_truth_types(cls) -> Tuple[Type]:
        """Return python builtin truth types."""
        return cls.__builtin_truth_types

class Recurser(metaclass=TypeHandler):
    @classmethod
    def rnamespace(
        cls,
        val: Any, 
        convert_nonbuiltins: bool = False,
        nested_namespaces: bool = False,
        _counter: int = 0,
    ) -> Any:
        """Recursively change nested dictionary values to namespace
        
        :param convert_nonbuiltins: convert nested objects outside of builtin objects
        :param nested_namespaces: convert nested dictionaries to namespaces
        :param _counter: internal variable for tracking iterations
        :return: SimpleNamespace converted representation of data structure
        """
        # Handle Non Standard Builtin Types
        def unknown_handler():
            condition = lambda t, x: not any([x.startswith("_"), callable(getattr(t, x))])
            if not hasattr(val, "__dict__"):
                return str(val)
            elif (_counter == 0) or (convert_nonbuiltins and nested_namespaces):
                return SimpleNamespace(**{
                    x: rcall(getattr(val, x)) for x in dir(val) if condition(val, x)
                })
            elif convert_nonbuiltins and not nested_namespaces:
                return {
                    x: rcall(getattr(val, x)) for x in dir(val) if condition(val, x)
                }
            else:
                return val

        # Handle Dictionaries
        def dictionary_handler():
            if nested_namespaces:
                return SimpleNamespace(**{k: rcall(v) for k, v in val.items()})
            else:
                return {k: rcall(v) for k, v in val.items()}
    
        # Prepare Recursive Call
        rcall = partial(
            cls.rnamespace, 
            convert_nonbuiltins=convert_nonbuiltins,
            nested_namespaces=nested_namespaces,
            _counter=(_counter+1),
        )

        # Handle Data Structures
        if isinstance(val, cls.binary_types):
            return str(val, cls.encoding)
        elif isinstance(val, cls.mapping_types):
            return dictionary_handler()
        elif isinstance(val, cls.iterable_types):
            return [rcall(x) for x in val]
        elif isinstance(val, cls.constant_types):
            return val
        else:
            return unknown_handler()

    @classmethod
    def rdict(
        cls,
        val: Any, 
        convert_nonbuiltins: bool = False, 
        _counter: int = 0,
    ) -> Any:
        """Recursively change nested objects to dictionary values
        
        :param convert_nonbuiltins: convert nested objects outside of builtin objects
        :param _counter: internal variable for tracking iterations
        :return: dictionary converted representation of data structure
        """
        # Handle Non Standard Builtin Types
        def unknown_handler():
            condition = lambda t, x: not any([x.startswith("_"), callable(getattr(t, x))])
            if not hasattr(val, "__dict__"):
                return str(val)
            if _counter == 0 or convert_nonbuiltins:
                return {x: rcall(getattr(val, x)) for x in dir(val) if condition(val, x)}
            else:
                return val

        # Prepare Recursive Call
        rcall = partial(
            cls.rdict, 
            convert_nonbuiltins=convert_nonbuiltins,
            _counter=(_counter+1),
        )

        # Handle Data Structures
        if isinstance(val, cls.binary_types):
            return str(val, cls.encoding)
        elif isinstance(val, cls.mapping_types):
            return {k: rcall(v) for k, v in val.items()}
        elif isinstance(val, cls.iterable_types):
            return [rcall(x) for x in val]
        elif isinstance(val, cls.constant_types):
            return val
        else:
            return unknown_handler()
   
    @classmethod
    def rsnaked(cls, val: Any) -> Any:
        """Recursively change keys to snake case within data structure"""
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
        """Convert a string to snake case"""
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
