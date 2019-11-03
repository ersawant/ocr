from datetime import datetime
import time
from flaskblog import db, login_manager
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    uploads = db.relationship('Submissions', backref='author', lazy=True)
    uploads2 = db.relationship('Submissions', backref='creator', lazy=True)



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.is_admin}')"



class Problem_statement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(db.Text, nullable=False, unique = True)


    def __repr__(self):
        return f"User('{self.id}', '{self.statement}')"



class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20))
    score = db.Column(db.Float)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Submissions('{self.filename}','{self.score}')"


class Allsubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(20))
    rouge = db.Column(db.Float, nullable=False)
    post_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"All Submissions('{self.user}','{self.file}', '{self.rouge}')"
