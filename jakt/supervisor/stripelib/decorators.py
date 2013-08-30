# coding=utf-8

import logging
logger = logging.getLogger(__name__)
from functools import wraps
from django.utils.decorators import available_attrs

def simple_shim (d, f=None):
    if callable(f):
        return d(f)
    return d

def decorator_shim (d, f, *a, **k):
    """Quick shim for the if func: return logic."""
    b = d(*a, **k)
    return simple_shim(b, f)

def stripe_call (func=None):
    def decorator (internal_func):
        @wraps(internal_func, assigned=available_attrs(internal_func))
        def _wrapped_view (*args, **kwargs):
            try:
                return internal_func(*args, **kwargs)
            except (Exception) as e:
                logger.exception(e)
                return None
        return _wrapped_view
    return simple_shim(decorator, func)
