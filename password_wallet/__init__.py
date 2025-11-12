from typing import Any
from icecream import ic
from flask import Flask
from password_wallet.config import DEBUG



def create_app() -> Flask:
    app = Flask(__name__)

    if not DEBUG:
            ic.disable()
    ic(f"Uruchamianie aplikacji {__name__} w trybie {'DEBUG' if DEBUG else 'PRODUCTION'}")
    
    app.config.from_pyfile("config.py")

    with app.app_context():
        from . import db
        db.init_app(app)

        from . import encryptions
        encryptions.init_app(app)

        from .blueprints.auth import bp as auth_bp
        app.register_blueprint(auth_bp)

        from .blueprints.home import bp as home_bp
        app.register_blueprint(home_bp)

    ic(f"Załadowano aplikację: {__name__}")
    return app
