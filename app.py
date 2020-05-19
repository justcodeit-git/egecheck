from models import Users, Posts
from routes import login_manager, app, current_user, g


@login_manager.user_loader
def load_user(user_id):
    return Users.get(Users.id == user_id)


@app.context_processor
def sidebar():
    # Вывод бокового сайдбара - Начало секции
    last_posts = Posts.select().order_by(Posts.create_date.desc()).limit(5)
    # Вывод бокового сайдбара - Конец секции
    return dict(last_posts=last_posts)


@app.context_processor
def need_info():
    # Определение статуса пользователя, система доступа - Начало секции
    u_status = ''
    u_id = 0
    u_name = ''
    u_surname = ''
    u_middle_name = ''
    u_nickname = ''
    g.user = current_user.get_id()
    user_info = Users.select().where(Users.id == g.user)
    for now_user in user_info:
        u_status = now_user.status
        u_id = now_user.id
    # Определение статуса пользователя, система доступа - Конец секции
    # Формирование ссылок на пользователей - Начало секции
    all_users = Users.select()
    for i in all_users:
        u_name = i.name
        u_surname = i.surname
        u_middle_name = i.middle_name
        u_nickname = i.nickname
    # Формирование ссылок на пользователей - Конец секции
    return dict(u_status=u_status, u_id=u_id, all_users=all_users, u_name=u_name, u_surname=u_surname,
                u_middle_name=u_middle_name, u_nickname=u_nickname)


if __name__ == '__main__':
    app.run(debug=True)
