import click
from . import create_app

@click.command()
@click.option("--debug", is_flag=True, default=False, help="Uruchom aplikację w trybie debugowania.")
def main(debug: bool):
    config = None
    if debug:
        from password_wallet.config import DebugConfig
        config = DebugConfig
    else:
        from password_wallet.config import ProdConfig
        config = ProdConfig

    app = create_app(config)
    app.run(debug=debug)

if __name__ == "__main__":
    main()
    