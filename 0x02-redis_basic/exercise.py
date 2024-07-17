#!/usr/bin/env python3
"""
exercise
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count calls to a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    client = redis.Redis()
    call_count = int(client.get(fn.__qualname__).decode('utf-8'))
    inputs = [i.decode('utf-8') for i in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [o.decode('utf-8') for o in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]

    print(f'{fn.__qualname__} was called {call_count} times:')
    for input_, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input_}) -> {output}')


class Cache:
    """
    Cache class using Redis.
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> any:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        data = self.get(key)
        if data is not None:
            return data.decode('utf-8')
        return None

    def get_int(self, key: str) -> Optional[int]:
        data = self.get(key)
        if data is not None:
            return int(data)
        return None
