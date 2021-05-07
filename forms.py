from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from db_models import User
import re


required_mes = "Это поле дожно быть заполнено"
pas_equel_mes = "Повторите пароль ещё раз"


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message=required_mes)])
    email = StringField('Почта', validators=[DataRequired(message=required_mes), Email(message='Некорректная почта')])
    password = PasswordField('Пароль', validators=[DataRequired(message=required_mes)])
    comfirm_password = PasswordField('Пароль ещё раз', validators=[DataRequired(), EqualTo('password', message=pas_equel_mes)])
    submit = SubmitField('Создать аккаунт')

    def validate_username(self, username):
        if not re.fullmatch(r"\w*", username.data):
            raise ValidationError("Имя пользователя может состоять только из букв и цифр")
        elif len(username.data) <= 3:
            raise ValidationError("Имя пользователя слишком короткое")
        elif len(username.data) >= 37:
            raise ValidationError("Имя пользователя слишком длинное")
        elif not re.fullmatch(r'[\da-zA-Z]*', username.data):
            raise ValidationError("Имя пользователя может содержать буквы только английского алфавита")
        elif User.query.filter(User.username == username.data).first():
            raise ValidationError("Пользователь с таким именем уже существует")

    def validate_password(self, password):
        if not re.fullmatch(r"[\w%]*", password.data):
            raise ValidationError("Пароль содержит зарещённые символы")
        elif len(password.data) <= 5:
            raise ValidationError("Пароль слишком короткий")
        elif len(password.data) >= 255:
            raise ValidationError("Пароль слишком длинный")

    def validate_email(self, email):
        if len(email.data) <= 3:
            raise ValidationError("Почта слишком короткая")
        elif len(email.data) >= 255:
            raise ValidationError("Почта слишком длинная")
        elif User.query.filter(User.email == email.data).first():
            raise ValidationError("Пользователь с такой почтой уже существует")



class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message=required_mes)])
    password = PasswordField('Пароль',  validators=[DataRequired(message=required_mes)])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        if not re.fullmatch(r"\w*", username.data):
            raise ValidationError("Неправильные логин или пароль")
        elif len(username.data) <= 3:
            raise ValidationError("Неправильные логин или пароль")
        elif len(username.data) >= 37:
            raise ValidationError("Неправильные логин или пароль")

    def validate_password(self, password):
        if not re.fullmatch(r"[\w%]*", password.data):
            raise ValidationError("Неправильные логин или пароль")
        elif len(password.data) <= 5:
            raise ValidationError("Неправильные логин или пароль")
        elif len(password.data) >= 255:
            raise ValidationError("Неправильные логин или пароль")


class PostForm(FlaskForm):
    title = StringField('Post title')
    content = TextAreaField('Post content')
    submit = SubmitField('Submit')



