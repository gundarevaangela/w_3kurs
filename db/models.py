from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    articles = relationship('articles', backref='author', lazy=True)
    opened_gifts = relationship('user_opened_gifts', backref='user', lazy=True)


class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer, default=0)


class gift_box(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pos_top = db.Column(db.Integer, nullable=False)
    pos_left = db.Column(db.Integer, nullable=False)
    is_opened = db.Column(db.Boolean, nullable=False, default=False)
    message = db.Column(db.String(255), nullable=True)
    requires_auth = db.Column(db.Boolean, nullable=False, default=False)  # Новое поле: требуется ли авторизация


class user_opened_gifts(db.Model):  # Новая модель
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gift_id = db.Column(db.Integer, db.ForeignKey('gift_box.id'), nullable=False)
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальный ключ, чтобы пользователь не мог открыть один подарок дважды
    __table_args__ = (db.UniqueConstraint('user_id', 'gift_id', name='unique_user_gift'),)