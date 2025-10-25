DEFAULT_KEY = 5
DESC = """
    Zmodyfikowana wersja syfru cezara.
    
    Zasada działanie jest taka sama z tą rużnicą że zamiast ogranicać się do danego alfabetu korzystamy z całej przestrzeni znaków
    dostepneji w UTF-8
"""

def encrypt(password: str, key: str) -> str:
    password_bytes: bytes = password.encode(encoding="UTF-8")
    
    try:
        key_int = int(key)
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e
    
    return bytes(map(lambda element: element + key_int, password_bytes)).decode()

def decrypt(encrypted_password: str, key: str) -> str:
    password_bytes: bytes = encrypted_password.encode(encoding="UTF-8")
    
    try:
        key_int = int(key)
    except ValueError as e:
        raise ValueError("Nie prawidłowy format klucza") from e

    return bytes(map(lambda element: element - key_int, password_bytes)).decode()