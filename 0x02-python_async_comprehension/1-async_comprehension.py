#!/usr/bin/env python3
"""Module for task 1."""
from typing import List
from importlib import import_module as using


async_generator = using('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """Creates a list of numbers from the an async number generator."""
    return [num async for num in async_generator()]
