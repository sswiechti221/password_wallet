import os
from typing import cast
from sqlmodel import SQLModel, Session, create_engine, select
from flask import Flask, current_app, g

from ._models_ import User, Encrypted_Password
from password_wallet import ic

DEBUG = current_app.config["DEBUG"]
DEBUG_DB = current_app.config["DEBUG_DB"]
DATABASE_FILE = current_app.config["DATABASE_FILE"]

engine = create_engine(DATABASE_FILE, echo=DEBUG and DEBUG_DB)

def open_session():
    if hasattr(g, "db_session"):
        raise RuntimeError("Sesja została ruż uruchomiona.")
    
    g.db_session = Session(engine)

def get_session() -> Session:
    if not hasattr(g, "db_session") or not g.db_session or not isinstance(g.db_session, Session):
        raise RuntimeError("Brak uruchomionej sesji")
    
    return cast(Session, g.db_session)

def close_session():
    if not hasattr(g, "db_session") or not isinstance(g.db_session, Session):
        raise RuntimeError("Brak uruchomionej sesji")
    
    g.db_session.close()
    g.pop("db_session", None)    

def create_db():
    SQLModel.metadata.create_all(engine)

def init_app(app: Flask):
    if not os.path.exists(DATABASE_FILE.removeprefix("sqlite:///")):
        create_db()
        ic(f"Baza danych nie istniała. Utworzono nową bazę danych: {DATABASE_FILE}")
    else:
        ic(f"Załadowano istniejącą bazę danych: {DATABASE_FILE}")
    
    ic(f"Zainicjowano moduł: {__name__}")

ic(f"Załadowano moduł: {__name__}")