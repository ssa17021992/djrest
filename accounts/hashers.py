from django.contrib.auth import hashers


class PBKDF2PasswordHasher(hashers.PBKDF2PasswordHasher):
    """PBKDF2 password hasher"""

    iterations = 100000
