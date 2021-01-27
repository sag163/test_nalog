from functools import wraps

from django.core.cache import cache


def get_cache_key(prefix, *args, **kwargs):
    hash_args_kwargs = hash(tuple(kwargs.items()) + args)
    return "{}_{}".format(prefix, hash_args_kwargs)


def cache_func(func, timeout=60, prefix=""):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = get_cache_key(prefix or func.__name__, *args, **kwargs)
        cached_value = cache.get(cache_key)
        if cached_value is None:
            cached_value = func(*args, **kwargs)
            cache.set(cache_key, cached_value, timeout)
        return cached_value

    return wrapper
