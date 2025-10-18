from flask import Blueprint, redirect, render_template, g, session, request

from password_wallet import ic
from password_wallet.config import AUTH_MAIN_PAGE, DEFAULT_REDIRECT_URL
from password_wallet.db import get_session, select, User

bp = Blueprint('auth', __name__, url_prefix='/auth')

def save_user(user: User):
    session['user_id'] = user.id
    session['user_signin'] = True
    
def clear_user():
    session.pop('user_id', None)
    session['user_signin'] = False

@bp.route('/')
def main():
    return render_template(AUTH_MAIN_PAGE)

@bp.post('signin')
def signin():
    user_login = request.form.get('user_login')
    user_password = request.form.get('user_password')
    
    if not user_login or not user_password:
        return render_template(AUTH_MAIN_PAGE, error_signin="Wypełnij wszystkie pola")
    
    with get_session() as db:
        query = select(User).where(User.login == user_login)
        user = db.exec(query).one_or_none()
        
        if not user:
            return render_template(AUTH_MAIN_PAGE, error_signin=f"Urzytkownik o loginie {user_login} nie istnieję")
        
        if user.password != user_password:
            return render_template(AUTH_MAIN_PAGE, error_signin="Nie prawidłowe hasło")
        
        save_user(user)
        
    return redirect(DEFAULT_REDIRECT_URL)

@bp.post('signup')
def signup():
    user_login = request.form.get('user_login')
    user_password = request.form.get('user_password')
    
    if not user_login or not user_password:
        return render_template(AUTH_MAIN_PAGE, error_signup="Wypełnij wszystkie pola")
        
    with get_session() as db:
        query = select(User).where(User.login == user_login)
        user = db.exec(query).one_or_none()
        
        if user:
            return render_template(AUTH_MAIN_PAGE, error_signup=f"Użytkownik o loginie {user_login} już istnieje")
        
        user = User(login=user_login, password=user_password)
        db.add(user)
        
        db.commit()
        
        save_user(user)
    
    return redirect(DEFAULT_REDIRECT_URL)

@bp.route('signout')
def signout():
    clear_user()
    return redirect(DEFAULT_REDIRECT_URL)

ic(f"Załadowano moduł: {__name__}")