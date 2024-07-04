#!/usr/bin/env python3
"""Module for task 11."""
from typing import Any, Mapping, Union, TypeVar


T = TypeVar('T')
Result = Union[Any, T]
Default = Union[T, None]


def safely_get_value(dct: Mapping, key: Any, default: Default = None) -> Result:
    """
    Retrieves a value from a dict using a given key.
    """
    if key in dct:
        return dct[key]
    else:
        return default
