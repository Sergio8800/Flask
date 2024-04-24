
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    posts = db.relationship('Comment', backref='author', lazy=True)  # без этого поля не получиться связать с моделью Пост.

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    img = db.Column(db.LargeBinary, nullable=False)
    img_way = db.Column(db.Text, nullable=False)

    # img = db.Column(db.Model)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Post({self.title}, {self.content}, {self.price})'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('goods.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Comment({self.content})'

class LoginForm(FlaskForm):
    username = StringField('name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Мужчина'), ('female', 'Женщина')])

#     собственный класс валидации
class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
