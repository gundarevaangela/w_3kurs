from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from datetime import datetime


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Добавляем поле для администратора
    
    # Связи с существующими моделями
    articles = relationship('articles', backref='author', lazy=True)
    opened_gifts = relationship('user_opened_gifts', backref='user', lazy=True)
    
    # Новые связи для системы инициатив
    initiatives = relationship('initiatives', backref='author', lazy=True)
    votes = relationship('votes', backref='voter', lazy=True)


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
    requires_auth = db.Column(db.Boolean, nullable=False, default=False)


class user_opened_gifts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    gift_id = db.Column(db.Integer, db.ForeignKey('gift_box.id'), nullable=False)
    opened_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'gift_id', name='unique_user_gift'),)


# ========== МОДЕЛИ ДЛЯ СИСТЕМЫ ИНИЦИАТИВ ==========

class initiatives(db.Model):
    """Модель для инициатив (предложений по улучшению)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь с голосами
    votes = relationship('votes', backref='initiative', lazy=True)


class votes(db.Model):
    """Модель для голосов за инициативы"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    initiative_id = db.Column(db.Integer, db.ForeignKey('initiatives.id'), nullable=False)
    vote_type = db.Column(db.Enum('up', 'down', name='vote_types'), nullable=False)
    
    # Один пользователь может голосовать за инициативу только один раз
    __table_args__ = (db.UniqueConstraint('user_id', 'initiative_id', name='unique_user_initiative_vote'),)