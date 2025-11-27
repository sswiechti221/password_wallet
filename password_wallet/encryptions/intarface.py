from typing import Any, Literal, Protocol, runtime_checkable

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
    CIPHER_TYPE: Literal["STREAM", "BLOCK", "CLASSIC"]
    
    @staticmethod
    def encrypt(plain_text: password_t, key: key_t) -> tuple[encrypted_password_t, json_data_t]:
        ...
    
    @staticmethod
    def decrypt(encrypted_text: encrypted_password_t, key: key_t, data: json_data_t) -> str:
        ...