import importlib
import os
from typing import cast, Protocol, runtime_checkable

from icecream import ic

__avaible_encryption_methods: dict[str, "EncryptionMethod"] = {}

@runtime_checkable
class EncryptionMethod(Protocol):    
    @staticmethod
    def encrypt(str: str) -> str:
        ...
    
    @staticmethod
    def decrypt(str: str) -> str:
        ...

for module_name in os.listdir(__name__.replace('.', '\\')):
    if module_name.startswith("__"):
        continue
    
    module = importlib.import_module(f".{module_name.removesuffix(".py")}", __name__)
    
    if isinstance(module, EncryptionMethod):
        __avaible_encryption_methods[module_name] = cast(EncryptionMethod, module)
        ic(f"Zaimportowano metode szyfrowania: {module_name}")
    else:
        ic(f"Nie udało się zaimportować metody syfrowania: {module_name}")
    
    
    
    
 


