from base64 import b64decode, b64encode
from typing import Any

from password_wallet.encryptions.utils import hash_key

NAME = "RC4"
KEY_DEFAULT = "DEFUALT"
KEY_SIZE_BITS = 32
DESC = """

"""
CIPHER_TYPE = "STREAM"

def _stream_key(key: bytes):
    S: list[int] = [i for i in range(256)]
    key_len = len(key)
    
    j: int = 0
    for i in range(256):
        j = (S[i] + j + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    
    i: int = 0
    j: int = 0
    while True:
        i = (i + 1) % 256
        j= (j + S[i]) % 256
        
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) % 256]
def _rc4(text: bytes, key: bytes) -> bytearray:
    KEY_STREAM = _stream_key(key)
    out: bytearray = bytearray()
    
    for text_chunk in text:
        key_chunk = next(KEY_STREAM)

        out.append(text_chunk ^ key_chunk)
        
    return out   

def encrypt(plain_text: str, key: str) -> tuple[str, dict[str, Any]]:
    plain_text_bytes = plain_text.encode()
    key_hash = hash_key(key, KEY_SIZE_BITS)
    
    encrypted_text = _rc4(plain_text_bytes, key_hash)
    
    return (b64encode(encrypted_text).decode(), {})        
def decrypt(encrypted_text: str, key: str, data: dict[str, Any]) -> str:
    encrypted_text_bytes = b64decode(encrypted_text)
    key_hash = hash_key(key, KEY_SIZE_BITS)
    
    plain_text = _rc4(encrypted_text_bytes, key_hash)
    
    return  plain_text.decode()
    