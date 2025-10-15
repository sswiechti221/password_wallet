from typing import Literal
from flask import Flask, render_template

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_pyfile("config.py")

    with app.app_context():
        from . import db
        db.init_app(app)
    
    @app.route("/hellow_word")
    def hellow_word() -> Literal['Hellow Word']:
        return "Hellow Word"

    @app.route("/dodaji")
    def test() -> Literal['Dodano']:
        with db.get_session() as sestion:
            user = db.User(
                login="Adam",
                password="1234"
            )
            sestion.add(user)
            sestion.commit()
            
        
        return "Dodano"
        

    return app

if (__name__ == "__main__"):
    create_app().run()
    