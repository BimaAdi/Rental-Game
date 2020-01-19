from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Game

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

## Init admin
def init():
    print('initialize admin')
    hashed_password = generate_password_hash('12345678', method='sha256')
    new_user = User(username='admin', password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()

## route
from views import *
