from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, default=False)
    games = db.relationship('Game', backref='user', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), unique=True)
    deskripsi = db.Column(db.String(100))
    tanggal_pinjam = db.Column(db.Date())
    tanggal_kembali = db.Column(db.Date())
    is_rental = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    