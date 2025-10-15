import click
from sqlmodel import SQLModel, Session, create_engine
from flask import Flask, current_app

from . import _models
from ._models import User, Password, Encryption_Method

engine = create_engine(f"sqlite:///{current_app.config["DATABASE_FILE"]}.db", echo=True)
print(f"\u001b[31mZostało załadowane: {__name__}\u001b[39m]")

def get_session():
    return Session(engine)

@click.command("create-db")
def create_db():
    SQLModel.metadata.create_all(engine)

def init_app(app: Flask):
    app.cli.add_command(create_db)
