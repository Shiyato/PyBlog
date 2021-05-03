from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from langdetect import detect, detect_langs
import re

required_mes = "Это поле дожно быть заполнено"
pas_equel_mes = "Повторите пароль ещё раз"

#Список запрещённых слов для проверки текста на нецензурную лексику.
forbidden_words = ['arse','ass','ballsack','bastard','bitch','biatch',
                   'bloody','blowjob','bollock','bollok','boner','boob','bugger',
                   'bum','butt','clitor','cock','coon','crap','cunt','damn','dick',
                   'dyke','fag','feck','fellatio','felching','fuck','fudge',
                   'flange','hell','homo','jerk','jizz','knob',
                   'labia','lmao','lmfao','muff','nigga','omg','penis','piss','poop',
                   'prick','pube','pussy','queer','scrotum','shit','slut',
                   'smegma','spunk','tit','tosser','turd','twat','wank','whore','wtf',
                   'хуй','пизд','бля','еба']


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(message=required_mes)])
    email = StringField('Почта', validators=[DataRequired(message=required_mes), Email(message='Некорректная почта')])
    password = PasswordField('Пароль', validators=[DataRequired(message=required_mes)])
    comfirm_password = PasswordField('Пароль ещё раз', validators=[DataRequired(), EqualTo('password', message=pas_equel_mes)])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        if not re.fullmatch(r"\w*", username.data):
            raise ValidationError("Имя пользователя может состоять только из букв и цифр")
        elif len(username.data) <= 3:
            raise ValidationError("Имя пользователя слишком короткое")
        elif len(username.data) >= 37:
            raise ValidationError("Имя пользователя слишком длинное")
        elif detect(username) != 'en' or len(detect_langs(username)) > 1:
            raise ValidationError("Имя пользователя может содержать буквы только английского алфавита")
        else:
            for el in forbidden_words:
                if el in username:
                    raise ValidationError("Имя пользователя содержит нецензурную лексику")
                    break

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



