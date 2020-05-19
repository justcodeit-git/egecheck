from routes import app, request
from models import db, Users, Posts, Notification, CommentsH, CommentsS, Messages
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

admin = Admin(app)


