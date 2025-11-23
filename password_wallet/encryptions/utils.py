from __future__ import annotations
from typing import Literal, Sequence

type BitOrder = Literal["Big", "Little"]
class BitSet:
    def __init__(self, value: int, size: int, bit_order: BitOrder = "Big") -> None:
        """_summary_

        Args:
            value (int): Wartość początkowa
            size (int): Ilość bitów
        """        
        if not (bit_order == "Big" or bit_order == "Little") :
            raise TypeError(f"Nie opsługiwano rodza numerowanie bitów {bit_order}")
        
        self.__value: int = self._normalize_(value, size)
        self.size: int = size
        self.bit_order: BitOrder = bit_order   
        
        self.__clered__: bool = False
    @property
    def value(self):
        return self.__value    
    @value.setter
    def value(self, new_value: int):
        self.__value = new_value
        self.__clered__ = False
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: value: {self.value} size: {self.size} bit_order: {self.bit_order}>"
    def __add__(self, other: BitSet) -> BitSet:
        """ Dodaje do siebie Obiekty typu BitSet o tych samych rozmiarach

            Jeżeli rozmiary BitSet są różne spowodóje to wywołanie wyjątku.
            
        Args:
            other (BitSet): BitSet do dodania

        Returns:
            BitSet:
        """
        self._is_the_same_size_(other)
        return BitSet(self.value + other.value, self.size, self.bit_order)
    def __and__(self, other: BitSet) -> BitSet:
        return BitSet(self.value & other.value, self.size, self.bit_order) 
    def __or__(self, other: BitSet) -> BitSet:
        return BitSet(self.value | other.value, self.size, self.bit_order) 
    def __xor__(self, other: BitSet) -> BitSet:
        return BitSet(self.value ^ other.value, self.size, self.bit_order)
    def __lshift__(self, value: int) -> BitSet:
        return BitSet(self.value << value, self.size, self.bit_order)
    def __rshift__(self, value: int) -> BitSet:
        return BitSet(self.value >> value, self.size, self.bit_order)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, BitSet):
            return self.value == other.value
        
        raise TypeError(f"Nie można porównać z typem: {type(other)}")
    def _normalize_(self, value: int, size: int) -> int:
        return value % (2 ** size)
    def _is_the_same_size_(self, other: BitSet, raise_exception: bool = True) -> bool:
        if self.size == other.size:
            return True    
        elif not raise_exception:
            return False 
        raise ValueError(f"Nie można dodać {self} do {other} ponieważ {self.size==other.size=}")
    def to_bytes(self) -> bytes:
        size =  self.size // 8
        if not self.size % 8 == 0:
            size += 1

        return self.value.to_bytes(size)
    def get_bits(self, locations: Sequence[int] | slice[int] | slice[int, int, int], new_size: int | None = None) -> BitSet:
        """
            Wybiera podane bity w kolejność takiej samej jak podano

        Args:
            location (Sequence[int] | slice[int] | slice[int, int, int]): Numery bitów

        Returns:
            Bitset: _description_
        """
        out: int = 0
        if isinstance(locations, slice):
            stop = locations.stop
            if locations.start and locations.step:
                start = locations.start
                step = locations.step
            else:
                start = 1
                step = 1
            
            reverse: bool = False
            stop = stop if stop >= 0 else self.size + stop + 1
            
            if step > 0:
                step = step
            elif step < 0:
                step = -step
                reverse = True
            else:
                step = 1
            
            locations = [loc for loc in range(start, stop + 1, step)]
            if reverse:
                locations.reverse()
        
        if self.bit_order == "Big":
            for loc in locations:
                if loc > self.size or loc < 0:
                    raise ValueError()
                
                bit: int = self.value >> (self.size - loc) & 0b1
                out = out << 1 | bit
        else:
            raise NotImplementedError()

        return BitSet(out, new_size if new_size else self.size, self.bit_order)
    def split(self, size: int) -> list[BitSet]:
        """ Dzieli BitSet na kilka mniejszych. o podanym rozmiarze.

        Args:
            size (int): Wielkość pojedynczego BitSet

        Raises:
            NotImplementedError: Jeżeli nie możliwe jest podzielenie BitSet na równe bloki.

        Returns:
            tuple[BitSet, ...] | BitSet: _description_
        """
        out: list[BitSet] = []
        if size == self.size:
            out.append(self)
        
        elif self.size % size == 0:
            for count in range(self.size // size):
                index_start =  count * size
                index_end = index_start + size
                out.append(self.get_bits(slice(index_start, index_end, 1), size))
        
        else:
            raise NotImplementedError("")
        
        return out
    def clear(self):
        self.__value = 0
        self.__clered__ = True    
    def resize(self, new_size: int):
        self.size = new_size
        self.value = self._normalize_(self.value, new_size)
    def expand(self, other: BitSet, side: Literal["Left", "Right"] = "Right") -> BitSet:
        if not self.bit_order == other.bit_order:
            raise NotImplementedError()
        
        if side == "Left":
            raise NotImplementedError()
        elif side == "Right":
            new_value: int = self.value << other.size | other.value
            new_size: int = self.size + other.size
        else:
            raise ValueError()
        
        return BitSet(new_value, new_size, self.bit_order)
    def rotate(self, by: int) -> BitSet:
        by %= self.size
        out: int = 0
        
        if by == 0:
            return type(self)(self.value, self.size, self.bit_order)
        
        elif by > 0:
            out = (self.value << by) & ((2 ** self.size) - 1) | (self.value >> (self.size - by))
            
        elif by < 0:
            out = (self.value >> by) | (self.value << (self.size - by)) & ((2 ** self.size) - 1)
            
        return BitSet(out, self.size, self.bit_order)
