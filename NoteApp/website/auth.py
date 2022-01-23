from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from datetime import date
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


def age_calculator(birthday):
    today = (str(date.today()).split('-'))
    birthday = birthday.split('-')
    age = int(today[0]) - int(birthday[0]) - ((int(today[1]), int(today[2])) < (int(birthday[1]), int(birthday[2])))
    return True if age > 15 else False


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_input = request.form.get('username')
        password = request.form.get('password')

        user_1 = User.query.filter_by(username=login_input).first()
        user_2 = User.query.filter_by(email=login_input).first()

        if user_1 or user_2:
            user = user_1 if user_1 else user_2
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, please try again.", "warning")

        else:
            flash("We couldn't find your user, please try again.", "warning")
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/signup', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        year, month, day = birthday.split('-')
        password_1 = request.form.get('password')
        password_2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        user_2 = User.query.filter_by(username=username).first()

        if user:
            flash("Email already exists.", category="danger")

        elif user_2:
            flash("Username already exists.", category="danger")

        elif len(name) < 3:
            flash("Your name must be longer than 2 characters.", category="danger")

        elif len(username) < 3:
            flash("Your username must be longer than 3 characters.", category="danger")

        elif len(email) < 10:
            flash("Email has to be longer than 10 characters.", category="danger")

        elif not age_calculator(birthday):
            flash("You must be older than 15 years old to sign up.", category="danger")

        elif password_1 != password_2:
            flash("Your passwords don't match", category="danger")

        elif len(password_1) < 5:
            flash("Your password is too short.", category="warning")

        else:
            new_user = User(name=name, username=username, email=email, birthday=date(int(year), int(month), int(day)),
                            password=generate_password_hash(password_1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("You have signed up successfully", category="success")
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)
