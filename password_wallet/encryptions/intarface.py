from typing import Any, Protocol, runtime_checkable

password_t = str
encrypted_password_t = str
method_name_t = str
key_t = str
json_data_t = dict[str, Any]

@runtime_checkable
class Encryption_Method(Protocol): 
    NAME: str
    DESC: str
    DEFAULT_KEY: str 
    
    @staticmethod
    def encrypt(password: password_t, key: key_t) -> tuple[encrypted_password_t, json_data_t]:
        ...
    
    @staticmethod
    def decrypt(encrypted_password: encrypted_password_t, key: key_t, data: json_data_t) -> str:
        ...