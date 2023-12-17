from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db  = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MOHAMMED ASHFAAQ'
    # app.config['MONGO_URI'] = "mongodb+srv://muzammilashfaaq:Mymongodbpass@cluster0.zzpsuvz.mongodb.net/?retryWrites=true&w=majority"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = 'website/uploads'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Recipe

    create_databases(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_databases(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('creted database!')




