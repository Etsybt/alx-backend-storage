#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable

client = redis.Redis()


def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of a function with an expiration time.
    """
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(url: str) -> str:
            cache_key = f"count:{url}"
            client.incr(cache_key)
            cached_content = client.get(url)
            if cached_content:
                return cached_content.decode('utf-8')
            result = fn(url)
            client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator

@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches it with an expiration time.
    """
    response = requests.get(url)
    return response.text
