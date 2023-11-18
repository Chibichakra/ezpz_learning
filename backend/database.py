from flask_sqlalchemy import SQLAlchemy
import uuid
db = SQLAlchemy()



class User(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)

class Course(db.Model):
    # Fields
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))

class Chapter(db.Model):
    # Fields
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50))
    course_id = db.Column(db.Uuid, db.ForeignKey("course.id"))

def db_register(username, password):
    pass


