from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

## DB Schema
# initialize using python repl (on terminal type python)
# from app import db, init
# db.create_all()
# init()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), unique=True)
    deskripsi = db.Column(db.String(100))
    is_rental = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

## WTForm
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class GameForm(FlaskForm):
    id = IntegerField('id')
    nama = StringField('nama', validators=[InputRequired(), Length(min=1, max=50)])
    deskripsi = StringField('deskripsi', validators=[InputRequired(), Length(min=8, max=100)], widget=TextArea())
    is_rental = BooleanField('is_rental')


## Init admin
def init():
    print('initialize admin')
    hashed_password = generate_password_hash('12345678', method='sha256')
    new_user = User(username='admin', password=hashed_password, is_admin=True)
    db.session.add(new_user)
    db.session.commit()

## route
@app.route('/')
def index():
    return redirect(url_for('game_index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user: # is User exist?
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data) 
                return redirect(url_for('game_index'))
        flash('invalid password or username')
        return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
        flash('User has been created now you can login')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('game_index'))

## route game
@app.route('/game', methods=['GET'])
def game_index():
    all_game = Game.query.limit(10).all()
    return render_template('game/index.html', all_game=all_game, current_user=current_user)

@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_detail(game_id):
    if request.method == 'GET':
        detail_game = Game.query.filter_by(id=game_id).first()
        return render_template('game/detail.html', detail_game=detail_game, current_user=current_user)
    else:
        return '<h1> game berhasil dirental </h1>'

@app.route('/game/create', methods=['GET', 'POST'])
@login_required
def game_create():
    if current_user.is_admin:
        form = GameForm()
        if form.validate_on_submit():
            new_game = Game(nama=form.nama.data, deskripsi=form.deskripsi.data, is_rental=False)
            db.session.add(new_game)
            db.session.commit()
            return redirect(url_for('game_index'))
        return render_template('game/create.html', form=form, current_user=current_user)
    else:
        return redirect(url_for('game_index'))

@app.route('/game/update/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_update(game_id):
    if current_user.is_admin:
        form = GameForm()
        if form.validate_on_submit():
            updated_game = Game.query.filter_by(id=game_id).first()
            updated_game.nama = form.nama.data
            updated_game.deskripsi = form.deskripsi.data
            updated_game.is_rental = form.is_rental.data
            db.session.commit()
            return redirect(url_for('game_index'))
        else:
            game = Game.query.filter_by(id=game_id).first()
            form = GameForm(id=game.id, nama=game.nama, deskripsi=game.deskripsi, is_rental=game.is_rental)
            return render_template('game/update.html', form=form, current_user=current_user)
    else:
        return redirect(url_for('game_index'))

@app.route('/game/delete/<int:game_id>', methods=['POST'])
@login_required
def game_delete(game_id):
    if current_user.is_admin:
        deleted_game = Game.query.filter_by(id=game_id).first()
        db.session.delete(deleted_game)
        db.session.commit()
    return redirect(url_for('game_index'))

@app.route('/game/rental/<int:game_id>', methods=['GET'])
@login_required
def game_rental(game_id):
    return render_template('game/rental.html', current_user=current_user)

