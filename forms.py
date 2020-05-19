from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, DataRequired, Email, Optional, Length


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[Required()])
    password = PasswordField('Пароль', validators=[Required(), DataRequired()])
    submit = SubmitField('Войти на сайт')


class MessageForm(FlaskForm):
    theme = StringField('Тема сообщения', validators=[Required()])
    message = TextAreaField('Текст сообщения')
    submit = SubmitField('Отправить сообщение')
