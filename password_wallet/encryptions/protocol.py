from typing import Protocol, runtime_checkable

@runtime_checkable
class Encryption_Method(Protocol): 
      
    @staticmethod
    def encrypt(password: str, key: str) -> str:
        ...
    
    @staticmethod
    def decrypt(encrypted_password: str, key: str) -> str:
        ...