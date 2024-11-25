from flask_sqlalchemy import SQLAlchemy  
from flask_login import UserMixin  
from flask import current_app  
from sqlalchemy.ext.declarative import declared_attr  
from werkzeug.security import generate_password_hash, check_password_hash  

db = SQLAlchemy()  

# Миксин для добавления временных меток  
class TimestampMixin:  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  

class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(80), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password_hash = db.Column(db.String(200), nullable=False)  # Храните хеш пароля  
    groups = db.relationship('Group', secondary='user_group', backref='users')  

    def __init__(self, username, email, password):  
        self.username = username  
        self.email = email  
        self.set_password(password)  # Устанавливаем хэш пароля  

    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  # Хеширование пароля

    def check_password(self, password):  
        return check_password_hash(self.password_hash, password)  # Проверка пароля  

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

class Group(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), unique=True, nullable=False)  

    def __repr__(self):
        return f"<Group(name={self.name})>"

user_group = db.Table('user_group',  
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),  
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))  
)  

class NewsArticle(db.Model, TimestampMixin):  # Используем миксин  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(200), nullable=False)  
    content = db.Column(db.Text, nullable=False)  

    def __repr__(self):
        return f"<NewsArticle(title={self.title})>"

# Создаем группы в базе данных  
def create_groups():  
    if not Group.query.filter_by(name='common').first():
        common_group = Group(name='common')  
        db.session.add(common_group)  

    if not Group.query.filter_by(name='authors').first():
        authors_group = Group(name='authors')  
        db.session.add(authors_group)  

    db.session.commit()