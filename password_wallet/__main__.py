import click

from .config import Config, DebugConfig, ProdConfig
from . import create_app

@click.group()
def group():
    "Password Wallet CLI"

@group.command("run")
@click.option("--debug", is_flag=True, help="Uruchom aplikację w trybie debugowania.")
def run(debug: bool):
    "Uruchom aplikację Password Wallet."
    config: Config
    if debug:
        config = DebugConfig
    
    else:
        config = ProdConfig   
    
    app = create_app(config=config)
    app.run(debug=debug)

if __name__ == "__main__":
    group()