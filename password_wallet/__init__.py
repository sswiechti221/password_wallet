from icecream import ic
from flask import Flask, redirect
from .config import Config, ProdConfig, DebugConfig

def create_app(*_, debug: bool) -> Flask:
    app = Flask(__name__)
    
    config: Config
    if debug:
        config = DebugConfig
     
    else:
        config = ProdConfig 
    
    
    ic(f"Uruchamianie aplikacji z konfiguracją: {config}")
    
    app.config.from_object(config)

    def static_x(folder: str, filename: str):
        return app.send_static_file(f'{folder}/{filename}')
    
    @app.get('/static/img/<path:filename>')
    def static_img(filename: str):
        return static_x('img', filename)

    @app.get('/static/css/<path:filename>')
    def static_css(filename: str):
        return static_x('css', filename)
    
    @app.get('/static/js/<path:filename>')
    def static_js(filename: str):
        return static_x('js', filename)
    
    @app.route("/")
    def main():
        return redirect("/home/")
        
    with app.app_context():
        from . import db
        db.init_app(app)

        from . import encryptions
        encryptions.init_app(app)

        from .blueprints.auth import bp as auth_bp
        app.register_blueprint(auth_bp)

        from .blueprints.home import bp as home_bp
        app.register_blueprint(home_bp)
        
        from .blueprints.encryption import bp as encryption_bp
        app.register_blueprint(encryption_bp)

    ic(f"Załadowano aplikację: {__name__}")
    return app
