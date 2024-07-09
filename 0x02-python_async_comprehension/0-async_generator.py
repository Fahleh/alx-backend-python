#!/usr/bin/env python3
"""Module for task 0."""
import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None, None]:
    """Asynchornously generates enerates 10 numbers."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
