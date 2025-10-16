from icecream import ic
from typing import Literal
from flask import Flask, render_template

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_pyfile("config.py")
    
    if not app.config.get("DEBUG"):
        ic.disable()

    with app.app_context():
        from . import db
        db.init_app(app)  
        
        from . import encryptions      

    return app

if (__name__ == "__main__"):
    create_app().run()
    