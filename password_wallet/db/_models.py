from typing import Any
from sqlmodel import Field, Relationship, SQLModel, JSON, Column

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    
    login: str = Field(unique=True, index=True)
    password: str = Field(min_length=64, max_length=64)
        
    # Relacje
    stored_passwords: list["Encrypted_Password"] = Relationship(back_populates="user", cascade_delete=True)
       
class Encrypted_Password(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    
    password: str
    
    encryption_method_name: str
    encryption_method_key: str
    encryption_method_data: dict[str, Any] = Field(sa_column=Column(JSON))
    
    # Relacja
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="stored_passwords", cascade_delete=False)    
    
    