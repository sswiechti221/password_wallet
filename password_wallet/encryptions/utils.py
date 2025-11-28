from __future__ import annotations
from base64 import b64decode, b64encode
from hashlib import blake2b
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
        
        self.__value__: int = self._normalize_(value, size)
        self.__size_bits__: int = size
        self.bit_order: BitOrder = bit_order   
        
        self.__clered__: bool = False
    
    @property
    def value(self):
        return self.__value__ 
    @value.setter
    def value(self, new_value: int):
        self.__value__ = self._normalize_(new_value, self.size_bits)
        self.__clered__ = False
    @property
    def bytes(self):
        return self.value.to_bytes(self.size_bytes)
    
    @property
    def size_bits(self):
        return self.__size_bits__
    @property
    def size_bytes(self):
        size = self.__size_bits__ // 8
        if not self.__size_bits__ % 8 == 0:
            size += 1    
        
        return size
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: value: {self.value} size: {self.size_bits} bits bit_order: {self.bit_order} bytes: {self.to_bytes()}>"
    def __add__(self, other: BitSet) -> BitSet:
        """ Dodaje do siebie Obiekty typu BitSet o tych samych rozmiarach

            Jeżeli rozmiary BitSet są różne spowodóje to wywołanie wyjątku.
            
        Args:
            other (BitSet): BitSet do dodania

        Returns:
            BitSet:
        """
        self._is_the_same_size_(other)
        return BitSet(self.value + other.value, self.size_bits, self.bit_order)
    def __and__(self, other: BitSet) -> BitSet:
        return BitSet(self.value & other.value, self.size_bits, self.bit_order) 
    def __or__(self, other: BitSet) -> BitSet:
        return BitSet(self.value | other.value, self.size_bits, self.bit_order) 
    def __xor__(self, other: BitSet) -> BitSet:
        return BitSet(self.value ^ other.value, self.size_bits, self.bit_order)
    def __lshift__(self, value: int) -> BitSet:
        return BitSet(self.value << value, self.size_bits, self.bit_order)
    def __rshift__(self, value: int) -> BitSet:
        return BitSet(self.value >> value, self.size_bits, self.bit_order)
    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, BitSet):
            return self.value == other.value
        
        raise TypeError(f"Nie można porównać z typem: {type(other)}")
    def _normalize_(self, value: int, size: int) -> int:
        return value % (2 ** size)
    def _is_the_same_size_(self, other: BitSet, raise_exception: bool = True) -> bool:
        if self.size_bits == other.size_bits:
            return True    
        elif not raise_exception:
            return False 
        raise ValueError(f"Nie można dodać {self} do {other} ponieważ {self.size_bits==other.size_bits=}")
    
    @classmethod
    def from_bytes(cls, bytes: bytes | bytearray, size: int | None= None) -> BitSet:
        size = size if size else len(bytes) * 8
        return cls(int.from_bytes(bytes), size)
    def to_bytes(self) -> bytes:
        """
            Alias do BitSet.bytes
        """
        return self.bytes
    @classmethod
    def from_base64(cls, bytes: bytes | bytearray, size: int) -> BitSet:
        return cls.from_bytes(b64decode(bytes), size)
    def to_base64(self) -> bytes:
        return b64encode(self.value.to_bytes(self.size_bits))
    
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
            stop = stop if stop >= 0 else self.size_bits + stop + 1
            
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
                if loc > self.size_bits or loc < 0:
                    raise ValueError()
                
                bit: int = self.value >> (self.size_bits - loc) & 0b1
                out = out << 1 | bit
        else:
            raise NotImplementedError()

        return BitSet(out, new_size if new_size else self.size_bits, self.bit_order)
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
        missing: int = 0
        need_shrink: bool = False
        
        if not self.size_bits % size == 0:
            missing = size - (self.size_bits % size)
            self.growth(missing)
            need_shrink = True    
        
        if size == self.size_bits:
            out.append(self)
        
        else:
            for count in range(self.size_bits // size):
                index_start =  count * size
                index_end = index_start + size
                out.append(self.get_bits(slice(index_start, index_end, 1), size))
       
            if need_shrink:
                self.shrink(missing)            
        
        return out
    def clear(self):
        self.__value = 0
        self.__clered__ = True    
    def growth(self, by: int) -> None:
        self.__size_bits__ += by
    def shrink(self, by: int) -> None:
        self.__size_bits__ -= by
        self.value = self.value #TODO Normalizuje -> Zmienić na coś lepszego
    def resize(self, new_size: int):
        self.__size_bits__ = new_size
        self.value = self._normalize_(self.value, new_size)
    def expand(self, other: BitSet, side: Literal["Left", "Right"] = "Right") -> BitSet:
        """ Roszerza BitSet o kolejny BitSet. Istnieje możliowść wybrania po któreji srtonie ma zostać umieszczony

        Args:
            other (BitSet): _description_
            side (Literal[&quot;Left&quot;, &quot;Right&quot;], optional): _description_. Defaults to "Right".

        Raises:
            NotImplementedError: _description_
            ValueError: _description_

        Returns:
            BitSet: _description_
        """
        new_value: int
        new_size: int
        
        if not self.bit_order == other.bit_order:
            raise NotImplementedError()
        
        if side == "Left":
            new_value = other.value << self.size_bits | self.size_bits
            new_size = self.size_bits + other.size_bits
        elif side == "Right":
            new_value = self.value << other.size_bits | other.value
            new_size = self.size_bits + other.size_bits
        else:
            raise ValueError(f"Nie poprawny agrument {side=}")
        
        return BitSet(new_value, new_size, self.bit_order)
    def rotate(self, by: int) -> BitSet:
        """ Obraca BitSet o podaną wartość 

        Args:
            by (int): Jeżeli dodatnie obraca w lewą stronę. Natomiast gdy ujemne to w prawo

        Returns:
            BitSet: _description_
        """
        by %= self.size_bits
        out: int = 0
        
        if by == 0:
            return self
        
        elif by > 0:
            out = (self.value << by) & ((2 ** self.size_bits) - 1) | (self.value >> (self.size_bits - by))
            
        elif by < 0:
            out = (self.value >> by) | (self.value << (self.size_bits - by)) & ((2 ** self.size_bits) - 1)
            
        return BitSet(out, self.size_bits, self.bit_order)
    
def hash_key(key: str, size: int) -> bytes:
    return blake2b(key.encode(), digest_size=size).digest()
