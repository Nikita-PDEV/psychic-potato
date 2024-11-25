from flask_wtf import FlaskForm  # Импортируем класс FlaskForm из flask_wtf
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, DateField  # Импортируем необходимые поля
from wtforms.validators import DataRequired, Length, Email, EqualTo  # Импортируем валидаторы

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для ввода email с валидаторами
    password = PasswordField('Пароль', validators=[DataRequired()])  # Поле для ввода пароля с валидаторами
    submit = SubmitField('Войти')  # Кнопка для отправки формы

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=150)])  # Поле для ввода имени пользователя
    email = StringField('Email', validators=[DataRequired(), Email()])  # Поле для ввода email
    password = PasswordField('Пароль', validators=[DataRequired()])  # Поле для ввода пароля
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])  # Поле для подтверждения пароля
    submit = SubmitField('Зарегистрироваться')  # Кнопка для отправки формы регистрации

class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])  # Поле для ввода названия новостной статьи
    content = TextAreaField('Содержание', validators=[DataRequired()])  # Поле для ввода содержания статьи
    submit = SubmitField('Сохранить')  # Кнопка для сохранения статьи

class SearchForm(FlaskForm):
    title = StringField('Название статьи')  # Поле для поиска по названию статьи
    date = DateField('Дата создания', format='%Y-%m-%d')  # Поле для фильтрации по дате создания
    submit = SubmitField('Поиск')  # Кнопка для выполнения поиска