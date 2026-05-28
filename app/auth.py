from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('로그인 정보를 확인해주세요.')
        return redirect(url_for('auth.login'))

    # Basic 2FA simulation: redirect to a simple "Verify" page
    return redirect(url_for('auth.two_fa', user_id=user.id))

@auth.route('/2fa/<int:user_id>')
def two_fa(user_id):
    return render_template('auth/2fa.html', user_id=user_id)

@auth.route('/2fa/<int:user_id>', methods=['POST'])
def two_fa_post(user_id):
    code = request.form.get('code')
    # For simulation, any 6-digit code works
    if len(code) == 6:
        user = User.query.get(user_id)
        login_user(user)
        return redirect(url_for('main.profile'))
    else:
        flash('잘못된 인증 코드입니다.')
        return redirect(url_for('auth.two_fa', user_id=user_id))

@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('이미 등록된 이메일 주소입니다.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
