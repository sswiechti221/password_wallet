from __future__ import annotations

import importlib
import os

from password_wallet import ic, Flask
from .protocol import Encryption_Method

__avaible_encryption_methods__: dict[str, Encryption_Method] = {}
__sorce_file__: str = "src" 

type password_t = str
type encrypted_password_t = str
type method_name_t = str
type key_t = str

def avaible() -> list[str]:
    return list(__avaible_encryption_methods__.keys())

def get(method_name: method_name_t) -> Encryption_Method:
    encryption_method =  __avaible_encryption_methods__.get(method_name, None)
    
    if encryption_method is None:
        raise RuntimeError(f"Nie znaleziono metody szyfrowania o nazwie: {method_name}")
    
    return encryption_method

def encrypt(method_name: method_name_t, password: password_t, key: key_t) -> encrypted_password_t:
    encrypted_password: encrypted_password_t =  get(method_name=method_name).encrypt(password=password, key=key)
    ic(f"Zaszyfrowano hasło. Hasło: {password} --> {encrypted_password} Metoda: {method_name} Kluczem: {key}")
    return encrypted_password

def decrypt(method_name: method_name_t, encrypted_password: encrypted_password_t, key: key_t) -> password_t:
    password = get(method_name=method_name).decrypt(encrypted_password, key)
    ic(f"Odszyfrowano hasło. Hasło: {encrypted_password} --> {password} Metoda: {method_name} Kluczem: {key}")
    return password

def init_app(app: Flask):
    for name in os.listdir(os.path.join(os.path.dirname(__file__), __sorce_file__)):
        name = name.removesuffix(".py")
        if name.startswith("__") and name.endswith("__"):
            continue    
        module = importlib.import_module(f".{__sorce_file__}.{name}", __name__)
        
        if isinstance(module, Encryption_Method):
            __avaible_encryption_methods__[name] = module
            
        ic(f"Załadowano metode szyfrowania: {name}")    
    ic(f"Zainicjowano moduł: {__name__}")        
ic(f"Załadowano moduł: {__name__}")

