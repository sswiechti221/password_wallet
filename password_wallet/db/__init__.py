import click

from sqlmodel import SQLModel, Session, create_engine, select
from flask import Flask

from . import _models
from ._models import User, Password, Encryption_Method
from password_wallet import ic
from password_wallet.config import DATABASE_FILE, DEBUG

engine = create_engine(f"sqlite:///{DATABASE_FILE}.db", echo=DEBUG)

def get_session():
    return Session(engine)

@click.command("create-db")
def create_db():
    SQLModel.metadata.create_all(engine)

def init_app(app: Flask):
    app.cli.add_command(create_db)

ic(f"Załadowano moduł: {__name__}")