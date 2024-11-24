from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from backend import bcrypt
from backend.models import db, User

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if User.query.filter_by(username=username).first():
            flash('Nazwa użytkownika już istnieje.', category='error')
        elif User.query.filter_by(email=email).first():
            flash('Email już istnieje.', category='error')
        elif password != confirm_password:
            flash('Hasła nie pasują do siebie.', category='error')
        else:
            new_user = User(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(password).decode("utf-8"),
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)

            flash('Rejestracja zakończona sukcesem! Możesz się zalogować.', category='success')
            return redirect(url_for('core_bp.home'))

    return render_template('auth/register.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            flash("Sprawdź dane logowania i spróbuj ponownie.", category="error")
            return redirect(url_for("auth_bp.login"))

        flash("Zalogowano pomyślnie!", category="success")
        login_user(user, remember=True)
        return redirect(url_for("core_bp.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Wylogowany', 'info')
    return redirect(url_for('auth_bp.login'))