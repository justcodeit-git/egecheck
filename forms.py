from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, DataRequired, Email, Optional, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Адрес электронной почты', validators=[Required()])
    password = PasswordField('Пароль', validators=[Required(), DataRequired()])
    submit = SubmitField('Войти на сайт')


class MessageForm(FlaskForm):
    theme = StringField('Тема сообщения', validators=[Required()])
    message = TextAreaField('Текст сообщения')
    submit = SubmitField('Отправить сообщение')


class RegisterForm(FlaskForm):
    surname = StringField('Фамилия', validators=[Required()])
    name = StringField('Имя', validators=[Required()])
    middle_name = StringField('Отчество (при наличии)', validators=[Required()])
    status = SelectField(
        'Выберите то, кем вы являетесь (если вы одновремено и педагог и репетитор, то выберите ваш главный статус)',
        choices=[('Учащйися', 'Учащийся'), ('Педагог', 'Педагог'),
                 ('Эксперт', 'Эксперт'), ('Репетитор', 'Репетитор')])
    email = StringField('Адрес электронной почты', validators=[Required()])
    password = PasswordField('Введите пароль')
    repeat_pass = PasswordField('Повторите ввод пароля',
                                validators=[Required(), EqualTo('repeat_pass', message='Пароли не'
                                                                                       'совпадают')])
    phone = StringField('Номер телефона')
    submit = SubmitField('Зарегистрироваться на сайте')
