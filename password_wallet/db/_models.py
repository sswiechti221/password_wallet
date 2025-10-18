from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    
    login: str
    password: str 
    
    name: str | None = Field(default=None)
    lastname: str | None = Field(default=None)
    
    # Relacje
    saved_passwords: list["Password"] = Relationship(back_populates="user")
       
class Password(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    
    password: str
    
    # Relacja
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="saved_passwords")
    
    encryption_method: "Encryption_Method" = Relationship(back_populates="password") 
    
    
class Encryption_Method(SQLModel, table =  True):
    id: int | None = Field(default=None, primary_key=True, foreign_key="password.id")
    
    name: str
    key: str
    
    # Relacja
    password: Password = Relationship(back_populates="encryption_method")