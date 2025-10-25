from typing import cast
from flask import Blueprint, render_template, request, session, redirect, url_for, g, flash

from password_wallet import encryptions, ic
from password_wallet import db
from password_wallet.config import DEFAULT_REDIRECT_URL
from password_wallet.db import get_session, select, User, Encrypted_Password

bp = Blueprint("home", __name__)

@bp.before_request
def db_and_user():
    db.open_session()
    
    if not session.get('user_signin', default=False) or not session.get('user_id', default=False):
        return redirect(url_for('auth.main'))
    
    user_id: int = session['user_id']
    db_session = db.get_session()
    db_query = select(User).where(User.id == user_id)
    
    try:
        g.user = db_session.exec(db_query).one()
    except Exception as e:
        from password_wallet.blueprints.auth import clear_user
        clear_user()
        ic(f"Nie znaleziono zalogowanego użytkownika w bazie danych: {e}")
        g.pop('user', None)
        
        return redirect(url_for('auth.main'))

@bp.after_request
def after_request(respond):
    db.close_session()   
    return respond
    
@bp.route("/blank")
def __blank() -> str:
    return render_template("base.html")

@bp.route("/")
def home():
    user = cast(User, g.user)
    avaible_encryptions = encryptions.avaible()
    stored_passwords: list[tuple[str, Encrypted_Password]] = [(encryptions.decrypt(encrypted_password.encryption_method_name, encrypted_password.password, encrypted_password.encryption_method_key), encrypted_password) for encrypted_password in user.stored_passwords]
    
    return render_template("home.html", avaible_encryptions=avaible_encryptions, stored_passwords=stored_passwords)

@bp.post('/store_password')
def store_password():
    password = request.form.get('password', type=str)
    encryption_method_name = request.form.get('encryption_method', default= None, type=str)
    encryption_method_key = request.form.get('encryption_key', default= None, type=str)
    
    info_redirect = redirect(url_for("home.home"))
    
    if not password or not encryption_method_name or not encryption_method_key:
        flash("Użupełnij wszystkie pola", "info")
        return info_redirect
    
    user: User = cast(User, g.user)
    if user.id is None:
        flash("Błąd: brak identyfikatora użytkownika", "error")
        return info_redirect

    encrypted_password = encryptions.encrypt(encryption_method_name, password, encryption_method_key)
    
    encrypted_password_db = Encrypted_Password(password=encrypted_password, encryption_method_name=encryption_method_name, encryption_method_key=encryption_method_key, user_id=user.id)

    db_session = db.get_session()
    db_session.add(encrypted_password_db)
    db_session.commit()
    
    return redirect(DEFAULT_REDIRECT_URL)

@bp.post("/dump_password")
def dump_password():
    encrypted_password_id = request.form.get("encrypted_password_id")
    user = cast(User, g.user)
    
    if not encrypted_password_id:
        raise RuntimeWarning("Próba usunięcia hasła które nie istnieje")
    
    encrypted_password_id = int(encrypted_password_id)
        
    db_session = db.get_session()
    db_query = db.select(Encrypted_Password).where(Encrypted_Password.user_id == user.id, Encrypted_Password.id == encrypted_password_id)
    encrypted_password = db_session.exec(db_query).one_or_none()
    
    if encrypted_password:
        db_session.delete(encrypted_password)
        db_session.commit()
        
    return redirect(url_for("home.home"))

ic(f"Załadowano moduł: {__name__}")