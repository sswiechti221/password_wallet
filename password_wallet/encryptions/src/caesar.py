from typing import Any
from base64 import b64encode, b64decode

NAME = "Caesar"
DEFAULT_KEY = "5"
DESC = """
    Zmodyfikowana wersja syfru cezara.
    
    Zasada działanie jest taka sama z tą rużnicą że zamiast ogranicać się do danego alfabetu. Operujemy na wartościach bajtów.
"""

def encrypt(password: str, key: str) -> tuple[str, dict[str, Any]]:
    password_bytes: bytes = password.encode(encoding="UTF-8")
    
    try:
        key_int = int(key , base=10)
        key_int = key_int % 256
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e
    
    return (b64encode(bytes(map(lambda element: (element + key_int) % 256, password_bytes))).decode(), {})

def decrypt(encrypted_password: str, key: str, data: dict[str, Any]) -> str:
    password_bytes: bytes = b64decode(encrypted_password.encode())
    
    try:
        key_int = int(key, base=10)
        key_int = key_int % 256
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e

    return bytes(map(lambda element: (element - key_int) % 256, password_bytes)).decode()