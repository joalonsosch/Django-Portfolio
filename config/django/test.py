from .base import *  # noqa: F403, F401

# Test-specific overrides
DEBUG = False
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
