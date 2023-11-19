from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(1000))

class Course(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

class Chapter(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))

def db_register(username, password):
    pass


