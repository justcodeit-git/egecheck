from datetime import datetime
from random import randint
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from transliterate import translit
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, Posts, Notification, CommentsH, CommentsS, Messages
from forms import LoginForm, MessageForm, RegisterForm
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

app = Flask(__name__)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'some secret key'

admin.add_view(ModelView(Users))
admin.add_view(ModelView(Posts))
admin.add_view(ModelView(CommentsH))
admin.add_view(ModelView(CommentsS))
admin.add_view(ModelView(Messages))
admin.add_view(ModelView(Notification))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    # Вывод всех постов - Начало секции
    public_posts = Posts.select().join(Users).where(Users.id == Posts.author).order_by(Posts.create_date.desc())
    # Вывод всех постов - Конец секции
    return render_template('index.html', public_posts=public_posts)


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    # Добавление и вывод комментариев - Начало секции
    post_id = Posts.get(Posts.id == id)
    form_h = CommentsHForm()
    form_s = CommentsSForm()
    if request.method == 'POST':
        current_category = Posts.select(Posts.category).where(Posts.id == post_id)
        for cat in current_category:
            if cat.category == 'История':
                k1h = request.form.get('k1h')
                k1h_grade = request.form.get('k1h_grade')
                k2h = request.form.get('k2h')
                k2h_grade = request.form.get('k2h_grade')
                k3h = request.form.get('k3h')
                k3h_grade = request.form.get('k3h_grade')
                k4h = request.form.get('k4h')
                k4h_grade = request.form.get('k4h_grade')
                k5h = request.form.get('k5h')
                k5h_grade = request.form.get('k5h_grade')
                k6h = request.form.get('k6h')
                k6h_grade = request.form.get('k6h_grade')
                k7h = request.form.get('k7h')
                k7h_grade = request.form.get('k7h_grade')
                total_h = int(k1h_grade) + int(k2h_grade) + int(k3h_grade) + int(k4h_grade) + int(k5h_grade) + int(
                    k6h_grade) + int(k7h_grade)
                g.user = current_user.get_id()
                create_date = datetime.today()
                post_id_h = post_id
                CommentsH.create(k1h=k1h, k2h=k2h, k3h=k3h, k4h=k4h, k5h=k5h, k6h=k6h, k7h=k7h,
                                 k1h_grade=k1h_grade, k2h_grade=k2h_grade, k3h_grade=k3h_grade,
                                 k4h_grade=k4h_grade, k5h_grade=k5h_grade, k6h_grade=k6h_grade,
                                 k7h_grade=k7h_grade, total=total_h, author=g.user, post_id=post_id_h,
                                 date=create_date)
                current_author_post = Posts.select(Posts).join(Users).where(Posts.id == post_id,
                                                                            Users.id == Posts.author)
                title = 'Ваше сочинение получило новую оценку'
                for j in current_author_post:
                    sender = Users.select().where(Users.id == g.user)
                    for i in sender:
                        message = i.surname + ' ' + i.name + ' оценил ваше историческое сочинение по периоду ' + j.title
                        recipient = j.author.id
                ntf_date = datetime.today()
                Notification.create(title=title, message=message, sender=sender, recipient=recipient, date=ntf_date)
                return redirect(request.url)
                print('YES HISTORY')
            elif cat.category == 'Обществознание':
                k1s = request.form.get('k1s')
                k1s_grade = request.form.get('k1s_grade')
                k2s = request.form.get('k2s')
                k2s_grade = request.form.get('k2s_grade')
                k3s = request.form.get('k3s')
                k3s_grade = request.form.get('k3s_grade')
                k4s = request.form.get('k4s')
                k4s_grade = request.form.get('k4s_grade')
                total_s = int(k1s_grade) + int(k2s_grade) + int(k3s_grade) + int(k4s_grade)
                g.user = current_user.get_id()
                create_date = datetime.today()
                post_id_s = post_id
                CommentsS.create(k1s=k1s, k2s=k2s, k3s=k3s, k4s=k4s, k1s_grade=k1s_grade, k2s_grade=k2s_grade,
                                 k3s_grade=k3s_grade,
                                 k4s_grade=k4s_grade, total=total_s, author=g.user, post_id=post_id_s, date=create_date)
                current_author_post = Posts.select(Posts).join(Users).where(Posts.id == post_id,
                                                                            Users.id == Posts.author)
                title = 'Ваше эссе получило новую оценку'
                for j in current_author_post:
                    sender = Users.select().where(Users.id == g.user)
                    for i in sender:
                        message = i.surname + ' ' + i.name + ' оценил ваше эссе на тему ' + j.title
                    recipient = j.author.id
                ntf_date = datetime.today()
                Notification.create(title=title, message=message, sender=sender, recipient=recipient, date=ntf_date)
                return redirect(request.url)
                print('YES SOCIAL')
    comments_h = CommentsH.select().join(Users).where(CommentsH.post_id == post_id,
                                                      Users.id == CommentsH.author).order_by(CommentsH.date.desc())
    comments_s = CommentsS.select().join(Users).where(CommentsS.post_id == post_id,
                                                      Users.id == CommentsS.author).order_by(CommentsS.date.desc())
    # Добавление и вывод комментариев - Конец секции
    return render_template("post.html", post=post_id, comments_h=comments_h, comments_s=comments_s, form_h=form_h)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    title = request.form.get('title')
    category = request.form.get('category')
    content = request.form.get('content')
    g.user = current_user.get_id()
    create_date = datetime.today()
    Posts.create(title=title, content=content, category=category, author=g.user, create_date=create_date)

    return redirect(url_for('index'))


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    rand_id = randint(0, 10)
    # Форма регистрации - Начало секции
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        middle_name = form.middle_name.data
        status = form.status.data
        email = form.email.data
        password = form.password.data
        repeat_password = form.repeat_pass.data
        phone_number = form.phone.data
        if not (name or surname or status or email or password or repeat_password):
            flash('Пожалуйста, заполните обязательные для регистрации поля')
        elif password != repeat_password:
            flash('Пароли не совпадают! Попробуйте ввести выбранный пароль ещё раз!')
        else:
            hash_pwd = generate_password_hash(password)
            Users.create(name=name, surname=surname, middle_name=middle_name, status=status, email=email,
                         password=hash_pwd, phone_number=phone_number, nickname=translit(str(name).lower()
                                                                                         + str(surname).lower()
                                                                                         + str(rand_id), 'ru',
                                                                                         reversed=True))
            return redirect(url_for('index'))
    # Форма регистрации - Конец секции
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Форма входа на сайт - Начало секции
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data and form.password.data:
            user_email = Users.get(Users.email == form.email.data)
            if form.email.data and check_password_hash(user_email.password, form.password.data):
                login_user(user_email)
                return redirect(url_for('index'))
            else:
                flash('Адрес электронной почты или пароль введены неверно. Попробуйте ещё раз.')
        else:
            flash('Вы не ввели адрес электронной почты или пароль')
    # Форма входа на сайт - Конец секции
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile/<nickname>', methods=['GET', 'POST'])
@login_required
def profile(nickname):
    # Используемые переменные
    user_surname = ''
    user_id = 0
    student_post_count = 0
    all_count = 0
    user_middle_name = ''
    user_name = ''
    user_nickname = ''
    user_status = ''
    user_email = ''
    user_phone = ''
    student_post_list = ''
    expert_comments_h = ''
    expert_comments_s = ''
    g.user = current_user.get_id()
    all_users = Users.select().where(Users.nickname == nickname)
    form = MessageForm()
    # Используемые переменные
    # Создание профилей пользователя - Начало секции
    for p_user in all_users:
        user_id = p_user.id
        user_name = p_user.name
        user_surname = p_user.surname
        user_middle_name = p_user.middle_name
        user_nickname = p_user.nickname
        user_status = p_user.status
        user_email = p_user.email
        user_phone = p_user.phone_number
        # Создание профилей пользователя - Конец секции
        # Работа с уведомлениями - Начало секции
    notification_list = Notification.select().join(Users, on=Notification.recipient).where(
        Notification.recipient == g.user).order_by(Notification.date.desc())
    notification_count = Notification.select().join(Users, on=Notification.recipient).where(
        Notification.recipient == g.user).count()
    # Работа с уведомлениями - Конец секции
    # Работа с личными сообщениями - Начало секции
    message_list = Messages.select().join(Users, on=Messages.recipient).where(
        Messages.recipient == g.user).order_by(Messages.date.desc())
    message_count = Messages.select().join(Users, on=Messages.recipient).where(
        Messages.recipient == g.user).count()
    # Работа с личными сообщениями - Начало секции
    # Вывод опубликованных учеником постов - Начало секции
    for student in all_users:
        if student.status == 'Учащийся':
            student_post_list = Posts.select().join(Users).where(Users.nickname == nickname)
            student_post_count = Posts.select().join(Users).where(Users.nickname == nickname).count()
        # Вывод опубликованных учеником постов - Конец секции
        # Вывод оценок, выставленных экспертом - Начало секции
    for expert in all_users:
        if expert.status == 'Педагог' or expert.status == 'Эксперт' or expert.status == 'Репетитор':
            expert_comments_h = CommentsH.select().join(Posts).where(CommentsH.post_id == Posts.id)
            expert_comments_s = CommentsS.select().join(Posts).where(CommentsS.post_id == Posts.id)
            expert_comments_h_count = CommentsH.select().join(Posts).where(CommentsH.post_id == Posts.id).count()
            expert_comments_s_count = CommentsS.select().join(Posts).where(CommentsS.post_id == Posts.id).count()
            all_count = expert_comments_h_count + expert_comments_s_count
            # Вывод оценок, выставленных экспертом - Конец секции
            # Форма отправки сообщения - Начало секции
    if request.method == "POST" and form.validate_on_submit():
        theme = form.theme.data
        message = form.message.data
        Messages.create(theme=theme, message=message, sender=g.user, recipient=user_id,
                        date=datetime.today())
        return redirect(request.url)
        # Форма отправки сообщения - Конец секции
    if user_id == g.user:
        return render_template('my_profile.html', user_surname=user_surname,
                               user_middle_name=user_middle_name, user_name=user_name, user_nickname=user_nickname,
                               user_status=user_status, user_email=user_email, user_phone=user_phone,
                               notification_list=notification_list, student_post_list=student_post_list,
                               expert_comments_h=expert_comments_h, expert_comments_s=expert_comments_s,
                               message_list=message_list, message_count=message_count,
                               notification_count=notification_count, student_post_count=student_post_count,
                               all_count=all_count)
    else:
        return render_template('user.html', user_surname=user_surname,
                               user_middle_name=user_middle_name, user_name=user_name, user_nickname=user_nickname,
                               user_status=user_status, user_email=user_email, user_phone=user_phone,
                               notification_list=notification_list, student_post_list=student_post_list,
                               expert_comments_h=expert_comments_h, expert_comments_s=expert_comments_s, form=form)
