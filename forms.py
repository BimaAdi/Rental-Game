from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.widgets import TextArea
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo

# use in login.html and views /login
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

# use in signup.html and views /signup
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

# use in game/create.html in views /game/create
class GameForm(FlaskForm):
    id = IntegerField('id')
    nama = StringField('nama', validators=[InputRequired(), Length(min=1, max=50)])
    deskripsi = StringField('deskripsi', validators=[InputRequired(), Length(min=8, max=100)], widget=TextArea())
    is_rental = BooleanField('is_rental')
    peminjam = StringField('nama_peminjam')
    tanggal_pinjam = DateField('tanggal_pinjam')
    tanggal_kembali = DateField('tanggal_kembali')

# use in game/rental.html and views /game/rental/<int:game_id>
class RentalForm(FlaskForm):
    user_id = IntegerField('user_id', render_kw={'readonly':True})
    game_id = IntegerField('game_id', render_kw={'readonly':True})
    nama_user = StringField('peminjam', render_kw={'readonly':True})# <--
    nama_game = StringField('nama game', render_kw={'readonly':True})
    # format='%d/%m/%Y'
    tanggal_pinjam = DateField('tanggal pinjam', validators=[DataRequired()])
    tanggal_kembali = DateField('tanggal kembali', validators=[DataRequired()])

# use in game/pengembalian.html and views /game/pengembalian/<int:game_id>
class PengembalianForm(FlaskForm):
    nama_game = StringField('nama game', render_kw={'readonly':True})
    nama_peminjam = StringField('nama peminjam', render_kw={'readonly':True})
    tanggal_pinjam = DateField('tanggal pinjam')
    tanggal_kembali = DateField('tanggal kembali')