from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    trips = db.relationship('Trip', backref='author', lazy=True)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)  # Широта
    longitude = db.Column(db.Float, nullable=True)  # Долгота
    description = db.Column(db.Text, nullable=False)
    cost = db.Column(db.Float, nullable=True)  # Стоимость путешествия
    image = db.Column(db.String(100), nullable=True)  # Путь к изображению
    transport_rating = db.Column(db.Integer, nullable=True)  # Оценка удобства передвижения
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
