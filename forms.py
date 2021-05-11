from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from db_models import User
from PIL import Image
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
        if not re.fullmatch(r'[\da-zA-Z]*', username.data):
            raise ValidationError("Имя пользователя может состоять только из цифр и букв английского алфавита")
        elif len(username.data) <= 3:
            raise ValidationError("Имя пользователя слишком короткое")
        elif len(username.data) >= 37:
            raise ValidationError("Имя пользователя слишком длинное")
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

class ProfileEdit(FlaskForm):
    photo = FileField('Фото профиля')
    username = StringField('Имя пользователя')
    description = TextAreaField('Описание профиля')
    submit = SubmitField('Подтвердить')

    def validate_username(self, username):
        if username.data:
            if not re.fullmatch(r'[\da-zA-Z]*', username.data):
                raise ValidationError("Имя пользователя может состоять только из цифр и букв английского алфавита")
            elif len(username.data) <= 3:
                raise ValidationError(f"Имя пользователя слишком короткое('{username.data}')")
            elif len(username.data) >= 37:
                raise ValidationError("Имя пользователя слишком длинное")
            elif User.query.filter(User.username == username.data).first() and username.data != current_user.username:
                raise ValidationError("Пользователь с таким именем уже существует")

    def validate_description(self, description):
        if len(description.data) > 500:
            raise ValidationError("Описание слишком длинное")

class PostForm(FlaskForm):
    title = StringField('Post title')
    content = TextAreaField('Post content')
    submit = SubmitField('Submit')



