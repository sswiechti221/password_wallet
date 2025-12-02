from icecream import ic
from flask import Flask
from .config import Config, DebugConfig


def create_app(config: Config = DebugConfig) -> Flask:
    app = Flask(__name__)
    
    ic(f"Uruchamianie aplikacji z konfiguracją: {config}")
    
    app.config.from_object(config)

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
