import pytest
from typing import Sequence
from password_wallet.encryptions import utils


@pytest.mark.parametrize("bitset, locations, expected", [
    (utils.BitSet(0b01100111, 8), slice(5), 0b01100),
    (utils.BitSet(0b01100111, 8), slice(1, -1, 1), 0b01100111),
    (utils.BitSet(0b01100111, 8), slice(1, -1, -1), 0b11100110),
    (utils.BitSet(0b01100111, 8), [1,2,3], 0b011),
    (utils.BitSet(0b01100111, 8), [3,2,1], 0b110),
    (utils.BitSet(0b01100111, 8), [3,1,2], 0b101)
])
def test_bitset_get_bits(bitset: utils.BitSet, locations: Sequence, expected):
    assert bitset.get_bits(locations).value == expected

@pytest.mark.parametrize("value, size, split_size, expected", [
    (0b1000, 4, 1, [1,0,0,0]),
    (0b1111, 4, 2, [3,3]),
    pytest.param(0b1010, 4, 3, [1, 2], marks=pytest.mark.xfail),
    (0b1111, 4, 4, [0b1111])
])
def test_bitset_split(value: int, size: int, split_size: int ,expected):
    
    for bitset, expected in zip(utils.BitSet(value, size).split(split_size), expected):
        assert bitset.value == expected

@pytest.mark.parametrize("value_a, size_a,  value_b, size_b, expected", [
    (10, 4, 10, 4, 4), (10, 4, -1, 4, 9)
    ])
def test_bitset_add(value_a: int, size_a: int,  value_b: int, size_b: int, expected):
    
    assert (utils.BitSet(value_a, size_a) + utils.BitSet(value_b, size_b)).value == expected

@pytest.mark.parametrize("value, size, by, expected", [
    (8, 4, 1, 0), (1, 4, 1, 2)
])
def test_bitset_lshift(value: int, size: int, by: int, expected):
    
    assert (utils.BitSet(value, size) << by).value == expected

@pytest.mark.parametrize("value, size, by, expected", [
    (0b10, 2, 0, 2), (0b10, 2, 1, 1), (0b10, 2, -1, 1), (0b10, 2, 2, 2), (0b10, 2, 3, 1),
    (0b010, 3, 0, 2), (0b010, 3, 1, 4), (0b010, 3, 2, 1), (0b010, 3, 3, 2)
])
def test_bitset_rotate(value: int, size: int, by: int, expected: int):
    bitset = utils.BitSet(value, size, "Big") 
    assert bitset.rotate(by).value == expected

