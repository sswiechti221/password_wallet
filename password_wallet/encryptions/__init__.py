import importlib
import os
from typing import cast, Protocol, runtime_checkable

from password_wallet import ic

__avaible_encryption_methods: dict[str, "Encryption_Method_Protocol"] = {}

@runtime_checkable
class Encryption_Method_Protocol(Protocol):    
    @staticmethod
    def encrypt(str: str, key: str) -> str:
        ...
    
    @staticmethod
    def decrypt(str: str, key: str) -> str:
        ...

def get_avaible_encryption_methods() -> dict[str, "Encryption_Method_Protocol"]:
    return __avaible_encryption_methods

for modul_name in os.listdir(__name__.replace('.', '\\')):
    if modul_name.startswith("__"):
        continue
    
    modul = importlib.import_module(f".{modul_name.removesuffix(".py")}", __name__)
    
    if isinstance(modul, Encryption_Method_Protocol):
        __avaible_encryption_methods[modul_name] = cast(Encryption_Method_Protocol, modul)
        ic(f"Zaimportowano metode szyfrowania: {modul_name}")
    else:
        ic(f"Nie udało się zaimportować metody syfrowania: {modul_name}")
        
ic(f"Załadowano moduł: {__name__}")
    
    
    
    
 


