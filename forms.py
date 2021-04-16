from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re

len_mes = "Длина имени должна быть в диапазоне от 4 до 33 символов"
equal_mes = "Повторите пароль ещё раз"
required_mes = "Это поле должно быть заполнено"

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message=required_mes), Length(min=4, max=33, message=len_mes)])
    email = StringField('Email', validators=[DataRequired(message=required_mes), Email(), Length(min=4, max=255, message=len_mes)])
    password = PasswordField('Password', validators=[DataRequired(message=required_mes), Length(min=4, max=33, message=len_mes)])
    comfirm_password = PasswordField('Comfirm Password', validators=[DataRequired(), EqualTo('password', message=equal_mes), Length(min=4, max=33, message=len_mes)])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if not re.fullmatch(r"[^\s\*\?\!\'\^\+\&amp;\/\(\)\=\}\]\[\{\$]*", username):
            raise ValidationError("Имя пользователя содержит запрещённые символы")

    def validate_password(self, password):
        if not re.fullmatch(r"[^\s\*\?\!\'\^\+\&amp;\/\(\)\=\}\]\[\{\$]*", password):
            raise ValidationError("Пароль содержит запрещённые символы")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message=required_mes), Length(min=4, max=33, message=len_mes)])
    password = PasswordField('Password',  validators=[DataRequired(message=required_mes), Length(min=4, max=33, message=len_mes)])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    title = StringField('Post title')
    content = TextAreaField('Post content')
    submit = SubmitField('Submit')



