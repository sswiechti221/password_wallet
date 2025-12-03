from typing import Any
from base64 import b64encode, b64decode

NAME = "Caesar"
KEY_DEFAULT = "5"
KEY_SIZE_BYTES = 1 # Nie istnieje fizyczny klucz, ale dla spójności z innymi szyframi definiujemy rozmiar 1 bajt
KEY_REGEX = r"^\d+$"
KEY_FORMAT = "Liczba całkowita reprezentująca przesunięcie liter w alfabecie (np. 3)"
DESC = """Jeden z najprostszych szyfrów podstawieniowych. Każda litera tekstu jawnego jest przesuwana o stałą liczbę pozycji w alfabecie (np. o 3). Bardzo łatwy do złamania – traktowany jako technika historyczna lub edukacyjna."""
CIPHER_TYPE = "CLASSIC"

def encrypt(plain_text: str, key: str) -> tuple[str, dict[str, Any]]:
    password_bytes: bytes = plain_text.encode(encoding="UTF-8")
    
    try:
        key_int = int(key , base=10)
        key_int = key_int % 256
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e
    
    return (b64encode(bytes(map(lambda element: (element + key_int) % 256, password_bytes))).decode(), {})

def decrypt(encrypted_text: str, key: str, data: dict[str, Any]) -> str:
    password_bytes: bytes = b64decode(encrypted_text)
    
    try:
        key_int = int(key, base=10)
        key_int = key_int % 256
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e

    return bytes(map(lambda element: (element - key_int) % 256, password_bytes)).decode()