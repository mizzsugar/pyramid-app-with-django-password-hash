"""This module is redistributed with modification from Django.
https://github.com/django/django/blob/master/django/utils/crypto.py
"""
import hashlib
import hmac
import secrets

from sample.libs.encoding import force_bytes


class InvalidAlgorithm(ValueError):
    """Algorithm is not supported by hashlib."""
    pass


def salted_hmac(
        key_salt: str,
        value: str,
        secret: str = None,
        algorithm: str = 'sha1',
):
    """
    Return the HMAC of 'value', using a key generated from key_salt and a
    secret (which defaults to settings.SECRET_KEY). Default algorithm is SHA1,
    but any algorithm name supported by hashlib.new() can be passed.

    A different key_salt should be passed in for every application of HMAC.
    """
    if secret is None:
        secret = 'settings.SECRET_KEY'

    key_salt = force_bytes(key_salt)
    secret = force_bytes(secret)
    try:
        hasher = getattr(hashlib, algorithm)
    except AttributeError as e:
        raise InvalidAlgorithm(
            '%r is not an algorithm accepted by the hashlib module.'
            % algorithm
        ) from e
    # We need to generate a derived key from our base key.  We can do this by
    # passing the key_salt and our base key through a pseudo-random function.
    key = hasher(key_salt + secret).digest()
    # If len(key_salt + secret) > block size of the hash algorithm, the above
    # line is redundant and could be replaced by key = key_salt + secret, since
    # the hmac module does the same thing for keys longer than the block size.
    # However, we need to ensure that we *always* do this.
    return hmac.new(key, msg=force_bytes(value), digestmod=hasher)


def get_random_string(length: int = 12, allowed_chars: str = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
)):
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    length = 12
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def constant_time_compare(val1: str, val2: str) -> bool:
    """Return True if the two strings are equal, False otherwise."""
    return secrets.compare_digest(force_bytes(val1), force_bytes(val2))


def pbkdf2(
        password: str,
        salt: str,
        iterations: int,
        dklen: int = 0,
        digest=None,
):
    """Return the hash of password using pbkdf2."""
    if digest is None:
        digest = hashlib.sha256
    dklen = dklen or None
    encoded_password = force_bytes(password)
    salt = force_bytes(salt)
    return hashlib.pbkdf2_hmac(
        digest().name, encoded_password, salt, iterations, dklen)