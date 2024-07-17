#!/usr/bin/env python3
"""
exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callabale) -> Callable:
    """
    takes a single method Callable
    argument and returns a Callable
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        called method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapperself._redis.incr(key)


class Cache:
    """
    class cache
    """
    def __init__(self):
        """
        initializes a cache obj
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stored data with a generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> any:
        """
        takes a key string argument and
        an optional Callable argument named fn
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        converts to a string
        """
        return data.decode('utf-8')

    def get_int(self, key: str) -> Optional[int]:
        """
        converts to an int
        """
        return int(data)
