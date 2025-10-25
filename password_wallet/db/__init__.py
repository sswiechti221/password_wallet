import click

from typing import cast
from sqlmodel import SQLModel, Session, create_engine, select
from flask import Flask, g

from ._models import User, Encrypted_Password
from password_wallet import ic
from password_wallet.config import DATABASE_FILE, DEBUG, DEBUG_DB

engine = create_engine(f"sqlite:///{DATABASE_FILE}", echo=DEBUG and DEBUG_DB)

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

@click.command("create-db")
def create_db():
    SQLModel.metadata.create_all(engine)

def init_app(app: Flask):
    app.cli.add_command(create_db)
    

ic(f"Załadowano moduł: {__name__}")