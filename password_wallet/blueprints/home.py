from flask import Blueprint, render_template, session, redirect, url_for, g

from password_wallet import ic
from password_wallet.db import get_session, select, User

bp = Blueprint("home", __name__)

@bp.before_request
def load_signined_user():
    if not session.get('user_signin', default=False):
        return
    
    user = session.get('user_id')
    
    if not user:
        g.user = None
    else:
        with get_session() as db:
            query = select(User).where(User.id == user)
            g.user = db.exec(query).one()
    
@bp.route("/blank")
def __blank() -> str:
    return render_template("base.html")

@bp.route("/")
def home():
    if not session.get('user_signin', default=False):
        return redirect(url_for('auth.main'))
    
    return render_template("home.html")

ic(f"Załadowano moduł: {__name__}")