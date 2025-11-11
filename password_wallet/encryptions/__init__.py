from __future__ import annotations

from ast import mod
import importlib
import os
from types import ModuleType

from password_wallet import ic, Flask
from .intarface import Encryption_Method, method_name_t, password_t, encrypted_password_t, key_t, json_data_t

__avaible_encryption_methods__: dict[str, Encryption_Method] = {}
__sorce_file__: str = "src" 

def avaible() -> list[str]:
    return list(__avaible_encryption_methods__.keys())

def get(method_name: method_name_t) -> Encryption_Method:
    encryption_method =  __avaible_encryption_methods__.get(method_name, None)
    
    if encryption_method is None:
        raise RuntimeError(f"Nie znaleziono metody szyfrowania o nazwie: {method_name}")
    
    return encryption_method

def encrypt(method_name: method_name_t, password: password_t, key: key_t) -> tuple[encrypted_password_t, json_data_t]:
    encrypted_password, json_data =  get(method_name=method_name).encrypt(password=password, key=key)
    ic(f"Zaszyfrowano hasło. Hasło: {password} --> {encrypted_password} Metoda: {method_name} Kluczem: {key}")
    return (encrypted_password, json_data)

def _encryption_method_test(module: Encryption_Method) -> bool:
    TEST_PASSWORD: password_t = "TEST_PASSWORD_1234!@#$"
    TEST_KEY: key_t = module.DEFAULT_KEY
    
    encrypted_password, data = module.encrypt(password=TEST_PASSWORD, key=TEST_KEY)
    decrypted_password = module.decrypt(encrypted_password=encrypted_password, key=TEST_KEY, data=data)
    
    if decrypted_password != TEST_PASSWORD:
        return False

    return True
    
def decrypt(method_name: method_name_t, encrypted_password: encrypted_password_t, key: key_t, data: json_data_t) -> password_t:
    password = get(method_name=method_name).decrypt(encrypted_password, key, data)
    ic(f"Odszyfrowano hasło. Hasło: {encrypted_password} --> {password} Metoda: {method_name} Kluczem: {key}")
    return password

def init_app(app: Flask):
    for file in os.listdir(os.path.join(os.path.dirname(__file__), __sorce_file__)):
        module_name = file.removesuffix(".py")
        if module_name.startswith("__") and module_name.endswith("__"):
            continue    
    
        module = importlib.import_module(f".{__sorce_file__}.{module_name}", __name__)
                    
        if not isinstance(module, Encryption_Method):
            ic(f"Moduł {module_name} nie implementuje interfejsu Encryption_Method. Pomijanie modułu.")
            continue
        
        if module_name in __avaible_encryption_methods__:
            ic(f"Metoda szyfrowania o nazwie {module_name} już istnieje. Pomijanie duplikatu.")
            continue
        
        try:
            if not _encryption_method_test(module):
                ic(f"Moduł {module_name} nie przeszedł testów poprawności. Pomijanie modułu. Hasło po zaszyfrowaniu i odszyfrowaniu nie zgadzało się.")
                continue
                    
        except Exception as e:
            ic(f"Wystąpił błąd podczas testowania modułu {module_name}. Pomijanie modułu. Błąd: {e}")
            continue  

        __avaible_encryption_methods__[module_name] = module
        ic(f"Załadowano metode szyfrowania: {module_name} => {module.NAME}")  
        
    ic(f"Zainicjowano moduł: {__name__}")        
ic(f"Załadowano moduł: {__name__}")

