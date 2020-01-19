from app import app, login_manager, db # render_template, redirect, url_for, request, flash,
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm, GameForm, RentalForm, PengembalianForm
from models import User, Game
from werkzeug.security import generate_password_hash, check_password_hash

## Index Route
@app.route('/')
def index():
    return redirect(url_for('game_index'))

## Authentication Route

# For login
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

# for signup
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

# for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('game_index'))

### Game Route
## Game CRUD

# Game index
@app.route('/game', methods=['GET'])
def game_index():
    all_game = Game.query.limit(10).all()
    return render_template('game/index.html', all_game=all_game, current_user=current_user)

# Game detail
@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    if request.method == 'GET':
        detail_game = Game.query.filter_by(id=game_id).first()
        return render_template('game/detail.html', detail_game=detail_game, current_user=current_user)
    else:
        return '<h1> game berhasil dirental </h1>'

# Game create
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

# Game update
@app.route('/game/update/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_update(game_id):
    if current_user.is_admin:
        form = GameForm()
        if form.validate_on_submit():
            updated_game = Game.query.filter_by(id=game_id).first()
            updated_game.nama = form.nama.data
            updated_game.deskripsi = form.deskripsi.data
            db.session.commit()
            return redirect(url_for('game_index'))
        else:
            game = Game.query.filter_by(id=game_id).first()
            form = GameForm(id=game.id, nama=game.nama, deskripsi=game.deskripsi)
            return render_template('game/update.html', form=form, current_user=current_user)
    else:
        return redirect(url_for('game_index'))

# Game delete
@app.route('/game/delete/<int:game_id>', methods=['POST'])
@login_required
def game_delete(game_id):
    if current_user.is_admin:
        deleted_game = Game.query.filter_by(id=game_id).first()
        db.session.delete(deleted_game)
        db.session.commit()
    return redirect(url_for('game_index'))

## Game extra route

# Game route for show form for rental game
@app.route('/game/rental/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_rental(game_id):
    form = RentalForm()
    if form.validate_on_submit():
        updated_game = Game.query.filter_by(id=game_id).first()
        updated_game.is_rental = True
        updated_game.tanggal_pinjam = form.tanggal_pinjam.data
        updated_game.tanggal_kembali = form.tanggal_kembali.data
        updated_game.user_id = form.user_id.data
        db.session.commit()
        return redirect(url_for('game_index'))
    nama_game = Game.query.filter_by(id=game_id).first().nama
    form = RentalForm(user_id=current_user.id, game_id=game_id, nama_user=current_user.username, nama_game=nama_game)
    return render_template('game/rental.html', form=form, current_user=current_user)

# Game route for show form for pengembalian game
@app.route('/game/pengembalian/<int:game_id>', methods=['GET', 'POST'])
@login_required
def game_pengembalian(game_id):
    if current_user.is_admin:
        form = PengembalianForm()
        if form.validate_on_submit():
            updated_game = Game.query.filter_by(id=game_id).first()
            updated_game.tanggal_pinjam = form.tanggal_pinjam.data
            updated_game.tanggal_kembali = form.tanggal_kembali.data
            db.session.commit()
            flash('Tanggal berhasil diganti!')
        game =  Game.query.filter_by(id=game_id).first()
        peminjam = User.query.filter_by(id=game.user_id).first()
        form = PengembalianForm(nama_game=game.nama, nama_peminjam=peminjam.username, 
                            tanggal_pinjam=game.tanggal_pinjam, tanggal_kembali=game.tanggal_kembali)
        return render_template('game/pengembalian.html', form=form, game=game)

    return redirect(url_for('game_index'))

# Game route for pengembalian specific game
@app.route('/game/pengembalian/selesai/<int:game_id>', methods=['GET'])
@login_required
def game_pengembalian_selesai(game_id):
    if current_user.is_admin:
        game_selesai = Game.query.filter_by(id=game_id).first()
        game_selesai.is_rental = False
        game_selesai.user_id = None
        game_selesai.tanggal_pinjam = None
        game_selesai.tanggal_kembali = None
        db.session.commit()
        return redirect(url_for('game_detail', game_id=game_selesai.id))
    return redirect(url_for('game_index'))
