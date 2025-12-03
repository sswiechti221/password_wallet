from __future__ import annotations
from base64 import b64encode, b64decode
from enum import  IntEnum
from functools import partial
from secrets import randbits
from typing import Any

from password_wallet.encryptions.utils import BitSet, hash_key

NAME = "Salsa20"
KEY_DEFAULT = "DOMYŚLNY_KLUCZ_SALSA20_HASZOWANY_SHA256"
KEY_SIZE_BYTES = 32
KEY_REGEX = r"^\w+$"
KEY_FORMAT = f"Tekstowy ciąg znaków pasujący do regexu: {KEY_REGEX}, który zostanie zahashowany do klucza o długości {KEY_SIZE_BYTES} bajtów"
DESC = """Nowoczesny, szybki i bezpieczny algorytm szyfrowania strumieniowego zaprojektowany przez Daniela Bernsteina. Generuje strumień pseudolosowych danych i łączy go z tekstem jawnym za pomocą XOR. Uważany za bardzo wydajny i bezpieczny, używany m.in. w kryptografii praktycznej (np. w systemach szyfrowania plików)."""
CIPHER_TYPE = "STREAM"

class Data_Size(IntEnum):
    BIT = 1
    BYTE = 8 * BIT
    
    WORD_BYTS = 4
    WORD_BITS = WORD_BYTS * BYTE
    
    BLOCK_WORDS = 16
    BLOCK_BYTS = BLOCK_WORDS * WORD_BYTS 
    BLOCK_BITS = BLOCK_BYTS * BYTE

word: partial[BitSet] = partial(BitSet, size=Data_Size.WORD_BITS.value)

def _litieendian(word: BitSet) -> BitSet:
    """
        (b1, b2, b3, b4) = (b4, b3, b2, b1) 
    """
    value: bytes = word.bytes
    new_value = bytes([value[3], value[2], value[1], value[0]])
    
    word.value = int.from_bytes(new_value)
    
    return word
def _quarterround(word_0: BitSet, word_1: BitSet, word_2: BitSet, word_3: BitSet) -> tuple[BitSet, BitSet, BitSet, BitSet]:
    """
    y1 = x1 XOR ((x0 + x3) <<< 7)
    y2 = x2 XOR ((y1 + x0) <<< 9)
    y3 = x3 XOR ((y2 + y1) <<< 13)
    y0 = x0 XOR ((y3 + y2) <<< 18)
    """
    
    word_1 = word_1 ^ ((word_0 + word_3).rotate(7))
    word_2 = word_2 ^ ((word_1 + word_0).rotate(9))
    word_3 = word_3 ^ ((word_2 + word_1).rotate(13))
    word_0 = word_0 ^ ((word_3 + word_2).rotate(18))
    
    return (word_0, word_1, word_2, word_3)
def  _rowround(words: list[BitSet]) ->list[BitSet]:
    """
    (y0, y1, y2, y3) = quarterround(x0, x1, x2, x3)
    (y5, y6, y7, y4) = quarterround(x5, x6, x7, x4)
    (y10, y11, y8, y9) = quarterround(x10, x11, x8, x9)
    (y15, y12, y13, y14) = quarterround(x15, x12, x13, x14)
    """
    if len(words) != 16:
        raise ValueError(f"Ocekiwano 16 słów (words), otrzymano {len(words)}")
    
    words[0], words[1], words[2], words[3] = _quarterround(words[0], words[1], words[2], words[3])
    words[5], words[6], words[7], words[4] = _quarterround(words[5], words[6], words[7], words[4])
    words[10], words[11], words[8], words[9] = _quarterround(words[10], words[11], words[8], words[9])
    words[15], words[12], words[13], words[14] = _quarterround(words[15], words[12], words[13], words[14])
    
    return words
def _collumnround(words: list[BitSet]) -> list[BitSet]:
    """
    (y0, y4, y8, y12) = quarterround(x0, x4, x8, x12)
    (y5, y9, y13, y1) = quarterround(x5, x9, x13, x1)
    (y10, y14, y2, y6) = quarterround(x10, x14, x2, x6)
    (y15, y3, y7, y11) = quarterround(x15, x3, x7, x11)
    """
    
    if len(words) != 16:
        raise ValueError(f"Ocekiwano 16 słów (words), otrzymano {len(words)}")

    words[0], words[4], words[8], words[12] = _quarterround(words[0], words[4], words[8], words[12])    
    words[5], words[9], words[13], words[1] = _quarterround(words[5], words[9], words[13], words[1])    
    words[10], words[14], words[2], words[6] = _quarterround(words[10], words[14], words[2], words[6])    
    words[15], words[3], words[7], words[11] = _quarterround(words[15], words[3], words[7], words[11])    

    return words
def _dubleround(words: list[BitSet]):
    if len(words) != 16:
        raise ValueError(f"Ocekiwano 16 słów (words), otrzymano {len(words)}")
    
    return _rowround(_collumnround(words))
def _hash(block: bytes):
    words: list[BitSet] = [_litieendian(word(int.from_bytes(block[index:index + 4]))) for index in range(0, 64, 4)]
    
    for _ in range(10):
        words = _dubleround(words)
    
    result = bytearray(64)
    for index, _word in enumerate(words):
        result[index * 4: index * 4 + 4] = _litieendian(_word).value.to_bytes(4)
        
    
    return bytes(result)
def _expand_key(key: bytes, nonce: bytes, block_numbrer: bytes):
    if len(key) not in (16, 32):
        raise ValueError(f"Nie prawidłowa długość klucza. Oczekiwono klucza długości (16, 32). Otrzymano: {len(key)}")
    
    data_block = bytearray()
    if len(key) == 16:
        constants= b"expand 16-byte k"
        
        data_block[0:4] = constants[0:4]
        data_block[4:20] = key
        data_block[20:24] = constants[4:8]
        data_block[24:32] = nonce
        data_block[32:40] = block_numbrer
        data_block[40:44] = constants[8:12]
        data_block[44:60] = key
        data_block[60:64] = constants[12:16]
         
        return _hash(data_block)
        
    elif len(key) == 32:
        constants = b"expand 32-byte k"

        data_block[0:4] = constants[0:4]
        data_block[4:20] = key[0:16]
        data_block[20:24] = constants[4:8]
        data_block[24:32] = nonce
        data_block[32:40] = block_numbrer
        data_block[40:44] = constants[8:12]
        data_block[44:60] = key[0:32]
        data_block[60:64] = constants[12:16]
        
        return _hash(data_block)
    
    raise ValueError("Nieprawidłowa długość klucza.")
def _get_nonce(size_bytes: int = 8) -> bytes:
    """ Generuje losowy ciag bajtów (nonce) o podanej długośći. 

    Args:
        size_bytes (int, optional): Długość nonce w bajtach. Domyślnie osiem bajtów.

    Returns:
        bytes: nonce
    """
    return randbits(size_bytes * Data_Size.BYTE.value).to_bytes(size_bytes)
def _salsa20(password_bytes: bytes, key_bytes: bytes, nonce: bytes) -> bytes:
    password_bytes_len: int = len(password_bytes)
    output: bytearray = bytearray()
    
    for block_number, block_index_start in enumerate(range(0, password_bytes_len, Data_Size.BLOCK_BYTS.value)):
        block_index_end = min(block_index_start + 64, password_bytes_len)
        
        expanded_key: bytes = _expand_key(key_bytes, nonce, block_number.to_bytes(8))
        
        for password_byte, key_byte in zip(password_bytes[block_index_start:block_index_end], expanded_key):
            output.append(password_byte ^ key_byte)
    
    return bytes(output)
    
def encrypt(plain_text: str, key: str) -> tuple[str, dict[str, Any]]:
    plain_text_bytes: bytes = plain_text.encode()
    key_hash: bytes = hash_key(key, KEY_SIZE_BYTES)
    
    nonce: bytes = _get_nonce()
    
    return (b64encode(_salsa20(plain_text_bytes, key_hash, nonce)).decode(), {"nonce": b64encode(nonce).decode()})   
def decrypt(encrypted_text: str, key: str, data: dict[str, Any]) -> str:
    encrypted_password_bytes: bytes = b64decode(encrypted_text)
    key_hash: bytes = hash_key(key, KEY_SIZE_BYTES)

    nonce = b64decode(data["nonce"])
    
    return _salsa20(encrypted_password_bytes, key_hash, nonce).decode()
