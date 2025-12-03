from flask import Blueprint, Response, flash, json, redirect, render_template, g, session, request, url_for
from hashlib import sha256

from password_wallet import db, ic
from password_wallet.config import AUTH_MAIN_PAGE, DEFAULT_REDIRECT_URL, HOME_PAGE_URL
from password_wallet.db import select, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def save_user(user: User):
    session['user_id'] = user.id
    session['user_signin'] = True
    
def clear_user():
    session.pop('user_id', None)
    session['user_signin'] = False

@bp.before_request
def before_request():
    db.open_session()

@bp.after_request
def after_request(request):
    db.close_session()
    
    return request

@bp.route('/')
def main():
    return render_template(AUTH_MAIN_PAGE)

@bp.post('signin')
def signin():
    user_login = request.form.get('user_login')
    user_password = request.form.get('user_password')
    
    if not user_login or not user_password:
        return Response(json.dumps({
                "type": "info",
                "message": "Wypełnij wszystkie pola"
            }),
            status=401)
    
    user_password_hash = sha256(user_password.encode())
    
    db_session = db.get_session()
    db_query = db.select(db.User).where(db.User.login == user_login, db.User.password == user_password_hash.hexdigest())
    user = db_session.exec(db_query).one_or_none()
    
    if not user:
        return Response(json.dumps({
                "type": "info",
                "message": "Niepoprawny login lub hasło"
            }),
            status=401)
    else:
        save_user(user)
        
    return redirect(HOME_PAGE_URL)

@bp.post('signup')
def signup():
    user_login = request.form.get('user_login')
    user_password = request.form.get('user_password')
    user_password_repet = request.form.get("user_password_repeat")
    
    if not user_password == user_password_repet:
        return Response(json.dumps({
                "type": "info",
                "message": "Hasła nie są identyczne"
            }),
            status=401)
    
    if not user_login or not user_password:
        return Response(json.dumps({
                "type": "info",
                "message": "Wypełnij wszystkie pola"
            }),
            status=401)
        
    db_session = db.get_session()
    db_query = select(User).where(User.login == user_login)
    user = db_session.exec(db_query).one_or_none()
    
    if user:
        return Response(json.dumps({
                "type": "info",
                "message": "Użytkownik o podanym loginie już istnieje"
            }),
            status=401)
    
    user_password_hash = sha256(user_password.encode())
    
    user = User(login=user_login, password=user_password_hash.hexdigest())
    db_session.add(user)
    db_session.commit()
    
    save_user(user)
    
    return redirect(DEFAULT_REDIRECT_URL)

@bp.route('signout')
def signout():
    clear_user()
    return redirect(DEFAULT_REDIRECT_URL)

ic(f"Załadowano moduł: {__name__}")