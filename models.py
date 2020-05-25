from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
from flask_login import UserMixin

db = PostgresqlDatabase(database='ege_check_base', user='postgres', password='24071990', host='localhost')
Messages = ''


class Users(Model, UserMixin):
    class Meta:
        database = db
        table_name = "users"

    name = CharField()
    surname = CharField()
    middle_name = CharField()
    nickname = CharField()
    status = CharField()
    email = CharField(unique=True)
    password = CharField()
    phone_number = CharField()


class Posts(Model):
    class Meta:
        database = db
        table_name = "posts"

    title = CharField()
    category = CharField()
    content = TextField()
    author = ForeignKeyField(Users, backref='posts_author')
    create_date = DateTimeField()
    is_published = BooleanField(default=True)


class Notification(Model):
    class Meta:
        database = db
        table_name = "notification"

    title = CharField()
    message = TextField()
    sender = ForeignKeyField(Users, backref='notify_sender')
    recipient = ForeignKeyField(Users, backref='notify_recipient')
    date = DateTimeField()
    status_view = BooleanField(default=False)


class CommentsH(Model):
    class Meta:
        database = db
        table_name = "comments_h"

    k1h_grade = IntegerField()
    k1h = CharField()
    k2h_grade = IntegerField()
    k2h = CharField()
    k3h_grade = IntegerField()
    k3h = CharField()
    k4h_grade = IntegerField()
    k4h = CharField()
    k5h_grade = IntegerField()
    k5h = CharField()
    k6h_grade = IntegerField()
    k6h = CharField()
    k7h_grade = IntegerField()
    k7h = CharField()
    total = IntegerField()
    date = DateTimeField()
    author = ForeignKeyField(Users, backref='history_comments')
    category = CharField(default='История')
    post_id = ForeignKeyField(Posts, backref='post_id_h')


class CommentsS(Model):
    class Meta:
        database = db
        table_name = "comments_s"

    k1s_grade = IntegerField()
    k1s = CharField()
    k2s_grade = IntegerField()
    k2s = CharField()
    k3s_grade = IntegerField()
    k3s = CharField()
    k4s_grade = IntegerField()
    k4s = CharField()
    total = IntegerField()
    date = DateTimeField()
    author = ForeignKeyField(Users, backref='social_comments')
    category = CharField(default='Обществознание')
    post_id = ForeignKeyField(Posts, backref='post_id_s')


class Messages(Model):
    class Meta:
        database = db
        table_name = "messages"

    sender = ForeignKeyField(Users, backref='message_sender')
    recipient = ForeignKeyField(Users, backref='message_recipient')
    theme = CharField()
    message = TextField()
    date = DateTimeField()
    is_read = BooleanField(default=False)


def init_db():
    db.connect()
    db.drop_tables([Users, Posts, CommentsH, CommentsS, Notification, Messages], safe=True)
    db.create_tables([Users, Posts, CommentsH, CommentsS, Notification, Messages], safe=True)
