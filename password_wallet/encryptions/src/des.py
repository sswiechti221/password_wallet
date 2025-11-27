from __future__ import annotations
from typing import Any
from password_wallet.encryptions.utils import BitSet

NAME = "Data Encryption Standard"
DESC = """"""
CIPHER_TYPE = "BLOCK"


BLOCK_SIZE = 8 * 8
BLOK_SIDE_SIZE = 4 * 8
KEY_SIDE_SIZE = 28
KEY_EXPANDED_SIZE = 6 * 8

type S_BOX_TABLE_t = tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]
S_BOXS_NUMBER: int = 8
S_BOXS_TABLE: list[S_BOX_TABLE_t] = [
    (
        (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
        (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
        (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
        (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13)
    ),
    (
        (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
        (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
        (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
        (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
    ),
    (
        (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
        (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
        (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
        (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
    ),
    (
        (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
        (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
        (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
        (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
    ),
    (
        (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
        (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
        (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
        (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
    ),
    (
        (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
        (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
        (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
        (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
    ),
    (
        (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
        (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
        (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
        (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
    ),
    (
        (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
        (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
        (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
        (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
    )
]

def _IP(block: BitSet) -> BitSet:
    """
        Permutacja początkowa DES -- IP 
    """    
    IP_TABLE: tuple[int, ...] = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    )
        
    return block.get_bits(IP_TABLE)
def _EP(block: BitSet) -> BitSet:
    EP_TABLE = (
    40,	8,	48,	16,	56,	24,	64,	32,
    39,	7,	47,	15,	55,	23,	63,	31,
    38,	6,	46,	14,	54,	22,	62,	30,
    37,	5,	45,	13,	53,	21,	61,	29,
    36,	4,	44,	12,	52,	20,	60,	28,
    35,	3,	43,	11,	51,	19,	59,	27,
    34,	2,	42,	10,	50,	18,	58,	26,
    33,	1,	41,	9,	49,	17,	57,	25,
    )
    
    return block.get_bits(EP_TABLE)

def _E(right_part: BitSet) -> BitSet:
    E_TABLE = (
        32, 1, 2, 3, 4, 5, 4, 5, 
        6, 7, 8, 9, 8, 9, 10, 11, 
        12, 13, 12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25, 24, 25, 26, 27, 
        28, 29, 28, 29, 30, 31, 32, 1
    )
    
    return right_part.get_bits(E_TABLE, 48) 
def _P(right_part: BitSet) -> BitSet:
    P_TABLE = (
        16,	7,	20,	21,	29,	12,	28,	17,
        1,	15,	23,	26,	5,	18,	31,	10,
        2,	8,	24,	14,	32,	27,	3,	9,
        19,	13,	30,	6,	22,	11,	4,	25,
    )
    
    return right_part.get_bits(P_TABLE)
def _PC_1(key: BitSet) -> tuple[BitSet, BitSet]:    
    PC_1_LEFT = (
        57,	49,	41,	33,	25,	17,	9,
        1,	58,	50,	42,	34,	26,	18,
        10,	2,	59,	51,	43,	35,	27,
        19,	11,	3,	60,	52,	44,	36
    )
    PC_1_RIGHT = (
        63,	55,	47,	39,	31,	23,	15,
        7,	62,	54,	46,	38,	30,	22,
        14,	6,	61,	53,	45,	37,	29,
        21,	13,	5,	28,	20,	12,	4
    )
            
    return key.get_bits(PC_1_LEFT, KEY_SIDE_SIZE), key.get_bits( PC_1_RIGHT, KEY_SIDE_SIZE)
def _PC_2(key: BitSet) -> BitSet:
    PC_2_TABLE = (
        14,	17,	11,	24,	1,	5,
        3,	28,	15,	6,	21,	10,
        23,	19,	12,	4,	26,	8,
        16,	7,	27,	20,	13,	2,
        41,	52,	31,	37,	47,	55,
        30,	40,	51,	45,	33,	48,
        44,	49,	39,	56,	34,	53,
        46,	42,	50,	36,	29,	32
    )
    return key.get_bits( PC_2_TABLE, KEY_EXPANDED_SIZE)
def _key_generator(key: bytes, rounds: int):
    key_bits = BitSet(int.from_bytes(key), 64, "Big")
    left_part, right_part = _PC_1(key_bits)
    
    KEY_SHIFT_TABLE = (
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    )
    
    for round_count in range(rounds):
        left_part = left_part.rotate(KEY_SHIFT_TABLE[round_count])
        right_part = right_part.rotate(KEY_SHIFT_TABLE[round_count])
        
        yield _PC_2(left_part.expand(right_part, "Right"))
       
def _S_BOX(S_BOX: int, value: BitSet) -> BitSet:
    y, x = value.get_bits([1,6]).value, value.get_bits([2, 3, 4, 5]).value
    return BitSet(S_BOXS_TABLE[S_BOX][y][x], 4)
def _F_function(right_part: BitSet, block_key: BitSet) -> BitSet:
    right_part = _E(right_part)
    right_part ^= block_key
    
    out: BitSet = BitSet(0, 32)
    
    for s_box, data in enumerate(right_part.split(6)):
            out = out << 4 | _S_BOX(s_box, data)
    
    if out.size_bits != 32:
        raise RuntimeError()
    
    return _P(out) 

def _des(text: bytes, key: bytes, decrypt: bool = False):
    block = BitSet(int.from_bytes(text), BLOCK_SIZE)
    
    block = _IP(block)
    
    left_part = block.get_bits(slice(1,32, 1), 32)
    right_part = block.get_bits(slice(33, -1, 1), 32)
    
    keys = list(_key_generator(key, rounds = 16))
    if decrypt:
        keys.reverse()
            
    for block_key in keys:        
        
        left_part ^= _F_function(right_part, block_key)
        
        left_part, right_part = right_part, left_part
        
    block = left_part.expand(right_part, "Right")
    block = _EP(block)
    
    return block.to_bytes()
        


if __name__ == "__main__":
    breakpoint()
    a = _des(b"siema", b"12345678")
    print(a)

    b = _des(a, b"12345678", True)
    print(b)
    
    pass