from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import datetime
import timeago

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'QWERTY123123'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/itstajyer1/PycharmProjects/pythonProject/web_note/database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, UpdateForm

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.jinja_env.filters['timeAgo'] = timeAgo

    return app


def create_database(app):
    if not path.exists('web_note/' + DB_NAME):
        db.create_all(app=app)


def timeAgo(date):
    return timeago.format(date.strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
