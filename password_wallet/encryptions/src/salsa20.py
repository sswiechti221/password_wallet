from __future__ import annotations
from enum import Enum
from functools import partial
from secrets import randbits
NAME = "Salsa20"

class Int_size(Enum):
    WORD = 4 * 8

class Finite_int():
    def __init__(self, value: int, size: Int_size | int) -> None:
        self.size: int = size.value if isinstance(size, Int_size) else size
        self.value: int = self._normalize(value)
    
    def _normalize(self, value: int) -> int:
        return value % (2 ** self.size)
    
    def __repr__(self) -> str:
        return f"<{__class__.__name__} size={self.size} value={self.value}>"
        
    def __add__(self, other: Finite_int) -> Finite_int:
        if self.size != other.size:
            raise ValueError(f"Nie można dodać {self.__repr__()} do {other.__repr__()}. Z powodu róznych rozmiarów {self.size == other.size = }")
        
        return Finite_int(self.value + other.value, self.size)
    
    def __xor__(self, other: Finite_int) -> Finite_int:
        if self.size != other.size:
            raise ValueError(f"Nie można dodać {self.__repr__()} do {other.__repr__()}. Z powodu róznych rozmiarów {self.size == other.size = }")
        
        return Finite_int(self.value ^ other.value, self.size)

    def __lshift__(self, by: int) -> Finite_int:
        
        return Finite_int(2**by * self.value % (2 ** self.size -1), self.size)

word = partial(Finite_int, size=Int_size.WORD)

def _litieendian(word: Finite_int) -> Finite_int:
    """
        (b1, b2, b3, b4) = (b4, b3, b2, b1) 
    """
    value: bytes = word.value.to_bytes(4)
    new_value = bytes([value[3], value[2], value[1], value[0]])
    
    word.value = int.from_bytes(new_value)
    
    return word

def _quarterround(word_a: Finite_int, word_b: Finite_int, word_c: Finite_int, word_d: Finite_int) -> tuple[Finite_int, Finite_int, Finite_int, Finite_int]:
    """
    y1 = x1 XOR ((x0 + x3) <<< 7)
    y2 = x2 XOR ((y1 + x0) <<< 9)
    y3 = x3 XOR ((y2 + y1) <<< 13)
    y0 = x0 XOR ((y3 + y2) <<< 18)
    """
    
    word_b = word_b ^ ((word_a + word_d) << 7)
    word_c = word_c ^ ((word_b + word_a) << 9)
    word_d = word_d ^ ((word_c + word_b) << 13)
    word_a = word_a ^ ((word_d + word_c) << 18)
    
    return (word_a, word_b, word_c, word_d)

def  _rowround(words: list[Finite_int]) ->list[Finite_int]:
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

def _collumnround(words: list[Finite_int]) -> list[Finite_int]:
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

def _dubleround(words: list[Finite_int]):
    if len(words) != 16:
        raise ValueError(f"Ocekiwano 16 słów (words), otrzymano {len(words)}")
    
    return _rowround(_collumnround(words))

def _hash(block: bytes):
    words: list[Finite_int] = [_litieendian(word(int.from_bytes(block[index:index + 4]))) for index in range(0, 64, 4)]
    
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
 
def _get_nonce(lenght: int = 8) -> bytes:
    """ Generuje losowy ciag bajtów (nonce) o podanej długośći. 

    Args:
        lenght (int, optional): Długość nonce w bajtach. Domyślnie osiem bajtów.

    Returns:
        bytes: nonce
    """
    return randbits(lenght * 8).to_bytes(lenght)
    
def encrypt(password: str, key: str) -> str:
    password_bytes: bytes = password.encode()
    key_bytes: bytes = key.encode()
    
    
    
    for block_number, block_index_start in enumerate(range(0, len(password_bytes), 64)):
        block_index_end = min(block_index_start + 64, len(password_bytes))
        
        nonce: bytes = _get_nonce()
        expanded_key: bytes = _expand_key(key_bytes, nonce, block_number.to_bytes(8))
    
            
    
    return "s"

def decrypt(password: str, key: str) -> str:
    return "s"
    

# key - 32/16 bytes
# nonce - 8 bytes
# block number - 8 bytes
