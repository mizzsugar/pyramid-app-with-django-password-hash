"""This module is redistributed with modification from Django.
https://github.com/django/django/blob/master/django/utils/encoding.py
"""
import datetime
from decimal import Decimal
from typing import Any

_PROTECTED_TYPES = (
    type(None),
    int,
    float,
    Decimal,
    datetime.datetime,
    datetime.date,
    datetime.time,
)


def is_protected_type(obj: Any) -> bool:
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_str(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


def force_bytes(
        s: Any,
        encoding: str = 'utf-8',
        strings_only: bool = False,
        errors: str = 'strict',
) -> bytes:
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, memoryview):
        return bytes(s)
    return str(s).encode(encoding, errors)
